import markup
import io


#simply pass transcript (txt file) through the main function and it will return marked-up file
def main(input):
    f = io.open('output.txt', mode='w')
    text = ''
    for i in input.read():
        if i != ' ' or i !='\n':
           text += i
    text = markup.homophone_replace(text)
    text = markup.ordinal_numbering(text)
    text = markup.percentage_repair(text)
    text = markup.de_sentence_breaks(text)
    f.write(text)
    f.close()
    return f

if __name__ == '__main__':
    main()