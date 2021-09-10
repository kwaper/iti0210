import os


def stopword(wstr):
    w = wstr.strip()
    if len(w) < 4:
        return True
    return False


def read_dir(dirn):
    cont_l = []
    for fn in os.listdir(dirn):
        with open(os.path.join(dirn, fn), encoding="latin-1") as f:
            words = [w.strip()
                     for w in f.read().replace("\n", " ").split(" ")
                     if not stopword(w)
                     ]
            cont_l.append(words)
    return cont_l


def connect_words(word_list):
    words = [w for sublist in word_list for w in sublist]
    return words


def count_words(list):
    word_count = {}
    for w in list:
        if w in word_count:
            word_count[w] = word_count[w] + 1
        else:
            word_count[w] = 1
    return word_count


def calculate_word_probability(word, word_frequency, all_words):
    return (word_frequency[word] + 1) / (len(all_words) + len(V))


def get_words_from_mail(mail):
    words = []
    splitted = mail.strip().replace("\n", " ").split(" ")
    for w in splitted:
        if not stopword(w) and w in spam_word_frequency and w in ham_word_frequency:
            words.append(w)
    return set(words)


def validate_mail(mail):
    ham = 0.0
    spam = 0.0
    words = get_words_from_mail(mail)
    for w in words:
        ham += calculate_word_probability(w, ham_word_frequency, all_ham_words)
        spam += calculate_word_probability(w, spam_word_frequency, all_spam_words)

    print(f"HAM CHANCE : {round(ham * 100, 5)} %")
    print(f"SPAM CHANCE : {round(spam * 100, 5)} %")

    if ham > spam:
        print("This mail is not SPAM.")
    else:
        print("This mail is SPAM.")


ham_l = read_dir(os.path.join("enron6", "ham"))
spam_l = read_dir(os.path.join("enron6", "spam"))

# print(len(ham_l), "ham messages")
# print(len(spam_l), "spam messages")

all_spam_words = connect_words(spam_l)
all_ham_words = connect_words(ham_l)

V = set(all_spam_words)  # all_spam_words: spam docs joined together
V.update(all_ham_words)
# print(len(V), "unique words")

spam_word_frequency = count_words(all_spam_words)
ham_word_frequency = count_words(all_ham_words)

kiri_1 = """
Subject: cleburne issues
daren , with megan gone i just wanted to touch base with you on the status of the enron payments owed to the cleburne plant . the current issues are as follows :
november gas sales $ 600 , 377 . 50
october payment to ena for txu pipeline charges $ 108 , 405 . 00
cleburne receivable from enron $ 708 , 782 . 50
less : november gas agency fees ( $ 54 , 000 . 00 )
net cleburne receivable from enron $ 654 , 782 . 50
per my discussions with megan , she stated that about $ 500 k of the $ 600 k nov gas sales was intercompany ( desk to desk ) sales , with the remainder from txu . are we able to settle any intercompany deals now ? are we able to settle with txu ?
additionally , you ' ll see that i included the oct txu payment in the receivable owed to cleburne also . this is because i always pay megan based upon the pipeline estimates in michael ' s file , even though they are not finalized until the next month . therefore in my november payment to enron , i paid ena for october ' s estimate , of which megan would have paid the final bill on 12 / 26 / 01 when it was finalized . however , i had to pay the october bill directly last month , even though i had already sent the funds to ena in november . therefore , i essentially paid this bill twice ( once to ena in nov & once to txu in dec ) . i deducted the november agency fees from these receivable totals to show the net amount owed to cleburne .
please advise as to the status of these bills . you can reach me at 713 - 853 - 7280 . thanks .
"""

kiri_2 = """
Subject: immediate contract payment .
immediate contract payment . our ref : cbn / ird / cbx / 021 / 05
attn :
during the auditing and closing of all financial records of the central bank of nigeria ( cbn ) it was discovered from the records of outstanding foreign contractors due for payment with the federal government of nigeria in the year 2005 that your name and company is next on the list of those who will received their fund .
i wish to officially notify you that your payment is being processed and will be released to you as soon as you respond to this letter . also note that from the record in our file , your outstanding contract payment is usd $ 85 , 000 , 000 . 00 ( eighty - five million united states dollars ) .
kindly re - confirm to me if this is inline with what you have in your record and also re - confirm the information below to enable this office proceed and finalize your fund remittance without further delays .
1 ) your full name .
2 ) phone , fax and mobile # .
3 ) company name , position and address .
4 ) profession , age and marital status .
5 ) copy of drivers license i . d .
as soon as the above information are received , your payment will be made available to you via an international certified bank draft , which will be delivered to your doorstep for your confirmation . you should call my direct number as soon as you receive this letter for further discussion and more clarification . also get back to me on this e - mail address ( payment _ info _ 10 @ yahoo . com ) and ensure that you fax me all the details requested to my direct fax number as instructed .
best regards ,
prof . charles c . soludo .
executive governor
central bank of nigeria ( cbn )
tel : 234 - 1 - 476 - 5017
fax : 234 - 1 - 759 - 0130
website : www . cenbank . org
mail sent from webmail service at php - nuke powered site
- http : / / yoursite . com
"""

validate_mail(kiri_2)
