import pyautogui
import pytesseract
import importlib
import requests
import html2text
from random import randint
import string
import pyscreenshot as ImageGrab
from googlesearch.googlesearch import GoogleSearch
try:
    import Image
except ImportError:
    from PIL import Image

stopwords = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about',
             'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be',
             'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself',
             'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each',
             'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his',
             'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down',
             'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had',
             'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been',
             'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because',
             'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you',
             'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those',
             'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a',
             'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']

ans_ind = 0
ycoord = 0
y_offset = 0

def get_text():
    global y_offset
    global stopwords

    lines_img = ImageGrab.grab(bbox = (1190, 800, 1191, 900))
    lines_img.save("lines.png")
    rgb_tot1 = 0
    rgb_tot2 = 0
    num_lines = 0
    for rgb in lines_img.getpixel((0, 20)):
        rgb_tot1 += rgb
    for rgb in lines_img.getpixel((0, 40)):
        rgb_tot2 += rgb

    #print(rgb_tot1, " " , rgb_tot2)

    if rgb_tot1 > 400 and rgb_tot2 > 400:
        num_lines = 4
    elif rgb_tot1 > 400:
        num_lines = 3
    else:
        num_lines = 2

    #print(num_lines)

    y_offset = (num_lines - 2) * 25

    q_img = ImageGrab.grab(bbox = (1190, 520,
                                   1530, 580 + y_offset))
    q_img.save("q.png")
    q_txt = pytesseract.image_to_string(Image.open("q.png")).replace("\n", " ")

    o1_img = ImageGrab.grab(bbox=(1200, 600 + y_offset,
                                  1480, 650 + y_offset))
    o1_img.save("o1.png")
    o1_txt = pytesseract.image_to_string(Image.open("o1.png"))

    o2_img = ImageGrab.grab(bbox=(1200, 660 + y_offset,
                                  1480, 705 + y_offset))
    o2_img.save("o2.png")
    o2_txt = pytesseract.image_to_string(Image.open("o2.png"))

    o3_img = ImageGrab.grab(bbox=(1200, 730 + y_offset,
                                  1480, 765 + y_offset))
    o3_img.save("o3.png")
    o3_txt = pytesseract.image_to_string(Image.open("o3.png"))

    output = [q_txt, o1_txt, o2_txt, o3_txt]
    output = [string.strip().lower() for string in output]


    '''
    q_img.show()
    o1_img.show()
    o2_img.show()
    o3_img.show()
    '''

    return output

def search(strings):

    print(strings[0])
    print("Options:\n" +
          strings[1] + "\n" +
          strings[2] + "\n" +
          strings[3] + "\n")


    response = GoogleSearch().search(strings[0])

    block = ""
    for result in response.results:
        try:
            block = block.join([result.title.lower() + " ", result.getText().lower()])
        except:
            continue
    stext = " ".join(block.split())
    
    '''


    block2 = ""
    urls = google.search(strings[0], num=20, stop=1)
    for url in urls:
        try:
            article = html2text.html2text(requests.get(url, timeout = 5).text)
            block2 = "".join([block2, " ", article.lower()])
        except:
            pass
    stext = " ".join(block.split())

    '''

    return stext, strings

def entire_option(stext, strings):

    occurances = [stext.count(strings[1]),
                  stext.count(strings[2]),
                  stext.count(strings[3])]

    highest_occ = max(occurances)
    ans_ind = occurances.index(highest_occ)

    if highest_occ != 0:
        print("Most likely is " + strings[ans_ind + 1] + " with " + str(highest_occ) + " occurances!")
        return ans_ind
    else:
        print("no match for 'entire option'")
        return -1

def partial_option(stext, strings):
    lists = []
    occurances = [0, 0, 0]
    for option in strings[1:]:
        option = option.translate(str.maketrans('', '', string.punctuation))
        lists.append(option.split(" "))


    for x in range(1, 3):
        lists[x] = [word for word in lists[x] if word not in stopwords]

        for word in lists[x]:
            occurances[x] += stext.count(word)

    highest_occ = max(occurances)
    ans_ind = occurances.index(highest_occ)

    if highest_occ != 0:
        print("Most likely is " + strings[ans_ind + 1] + " with " + str(highest_occ) + " occurances!")
        return ans_ind
    else:
        print("No match for 'partial option'")
        return -1


if __name__ == '__main__':

    #put path to tesseract executable here
    
    pytesseract.pytesseract.tesseract_cmd = r"C:\Users\tEST\AppData\Local\Tesseract-OCR\tesseract.exe"

    while True:

        pause = input("'y' to signal next question, 'exit' to exit")

        if pause == "exit":
            break

        qtext = get_text()
        stext, strings = search(qtext)

        '''
        DETERMINE ANSWER
        '''

        ans_ind = entire_option(stext, strings)

        if ans_ind == -1:
            ans_ind = partial_option(stext, strings)

        if ans_ind == -1:
            print("No answer found, choosing randomly")
            random.seed
            ans_ind = randint(0, 2)

        if ans_ind == 0:
            ycoord = 625 + y_offset
        elif ans_ind == 1:
            ycoord = 680 + y_offset
        else:
            ycoord = 750 + y_offset

        pyautogui.moveTo(1300, ycoord)
        pyautogui.click()
