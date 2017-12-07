# JHTC CTF Workshops / KNI Kernel AGH
This repo contains materials from [Just Hit the Core CTF team](https://ctftime.org/team/13830/) workshops organized thanks to [KNI Kernel](https://www.facebook.com/KNIKernel/) at [AGH University of Science and Technology](http://www.agh.edu.pl/en/).

As the workshops are in Polish, so are the materials here.

---

### Warsztaty w roku akademickim 2017/2018

#### 8.11.2017

Przerobiliśmy zadania z [mini CTFa od P4 z konferencji Security PWNing Conference 2017](https://pwning2017.p4.team/tasks):
* web100 captcha,
* web150 sprzedam flagę,
* crypto25 xor,
* re100 nieznany format

Omówiliśmy między innymi:
* działanie protokółu HTTP,
* jak skonfigurować proxy w przeglądarce (wykorzystaliśmy Burp Suite jako proxy),
* działanie nagłówka HSTS

Powiedzieliśmy również co nieco o LLVM, jego pośredniej reprezentacji kodu oraz podstawach asemblera (rejestry procesora, kilka instrukcji, na tyle, aby zrobić zadanie re100).

#### 15.11.2017 - warsztaty z eksploitowania lokalnych programów/binarek prowadzone przez Mateusza 'mawekl' Pstrusia.

[Przerobione zadania](https://securitytraps.pl/KNI/); prezentacja się tu dopiero pojawi.

#### 30.11.2017 - warsztaty z niskopoziomowej inżynierii wstecznej

- krótka prelekcja o podstawach asemblera x86/x64 - https://docs.google.com/presentation/d/1HKuW69NFD2IFSdkdD7ul3aWriHXHDLfPOvJV0wsiwH0 (pierwsze 17 slajdów)
- zreversowaliśmy zadanie https://challenges.re/1/
- zrobiliśmy trzy zadania z microcorruption.com/login

#### 7.12.2017 - warsztaty z kryptografii - protokół Diffiego-Hellmana

Materiały znajdują się w [2017/lab\_dh](/2017/lab_dh). Serwery z zadaniami można hostować lokalnie następującymi poleceniami:
```bash
git clone git@github.com:JustHitTheCore/ctf_workshops.git
python2 -m pip install pwntools pycrypto  # albo pip install ...
apt-get install socat  # musimy zainstalować program socat
cd ctf_workshops/2017/lab_dh/
source ./setup.sh
```

Zadania wykorzystują bibliotekę pwntools (stąd wczesniej ją instalujemy) - ma ona między innymi bardzo wygodny interfejs do socketów, stąd wykorzystujemy ją też do rozwiązań.

Kody z zajęć (nieskończone zadania z przedstawioną ideą):
* [task2\_mitm.py](/2017/lab_dh_done_on_labs/task2_mitm.py)
* [task4\_subgroup\_confinement.py](/2017/lab_dh_done_on_labs/task4_subgroup_confinement.py)

Treści zadań i więcej informacji jest [w README w materiałach z tych warsztatów](/2017/dh_labs/).

Więcej informacji pojawi się tu, gdy wrzuci je Gros (który prowadził warsztaty).

#### Kolejne spotkanie

**W czwartek 7.12.2017 o 18:00 w D10 226** - temat: kryptografia; warsztaty poprowadzi Gros z JHtC.

### Warsztaty w roku akademickim 2016/2017

Można je znaleźć w katalogu 2016 ;).


### Wanna join?

Just come to the workshops.


