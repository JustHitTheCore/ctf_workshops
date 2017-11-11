# https://pwning2016.p4.team/task/male_jest_piekne
import codecs


def bytes_to_long(data):
    return int(data.encode("hex"), 16)


def rsa_encrypt(msg, e, n):
    return pow(bytes_to_long(msg), e, n)


def main():
    n = 13513545201780754751363061730973412461964840798555163524204230289623875027547891
    e = 65537
    flag = "" # secret!
    with codecs.open("encrypted.txt", "w") as output_flag:
        output_flag.write(hex(rsa_encrypt(flag, e, n)))


main()
