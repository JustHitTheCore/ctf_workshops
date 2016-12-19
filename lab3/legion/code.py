# https://pwning2016.p4.team/task/legion
import codecs


def bytes_to_long(data):
    return int(data.encode("hex"), 16)


def rsa_encrypt(msg, e, n):
    return pow(bytes_to_long(msg), e, n)


def main():
    n = 29819592777931214269172453467810429868925511217482600306406141434158090
    e = 65537
    flag = "" #secret!
    with codecs.open("encrypted.txt", "w") as output_flag:
        output_flag.write(hex(rsa_encrypt(flag, e, n)))


main()
