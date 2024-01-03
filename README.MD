# Security By Design - Zadanie 3

## Wymagania
1. Zainstalowana komenda `git` na stacji roboczej
2. Zainstalowany `docker` na stacji roboczej
3. Bezpośredni dostęp do internetu (nie przez proxy)
4. Zainstalowany program `Postman` - https://www.postman.com

## Przygotowanie
1. **Założenie konta na GitHub** (jeśli jeszcze nie jesteś zarejestrowany)  
   Aby wykonać ćwiczenie, konieczne jest posiadanie zarejestrowanego użytkownika na portalu github.com.

2. **Wykonanie "fork'a" projektu**  
   Wykonaj "fork'a" projektu [https://github.com/Mixeway-Academy/task3](https://github.com/Mixeway-Academy/task3) - w wyniku tej operacji, w twojej przestrzeni na GitHubie powstanie kopia repozytorium.  
   Zadanie zakłada wykonanie listy operacji na kodzie źródłowym, ale aby nie wprowadzać zmian w przestrzeni, z której korzystają inni użytkownicy, wygodnie jest wykonać kopię w swojej przestrzeni. Więcej informacji znajdziesz [tutaj](https://docs.github.com/en/get-started/quickstart/fork-a-repo).  
   ![img.png](.github/img.png)

3. **Pobranie kopii projektu na swoją stację roboczą**
   Aby pobrać 'sforkowany' projekt na swoją stację roboczą, wykonaj poniższą komendę:

```shell
git clone https://github.com/{username}/task1

#gdzie {username} to nazwa użytkownika. Wchodząc w swoją kopie repozytoroium przez przeglądarkę można też skorzystać z adresu URL.
```
4. Zainstalowanie Postmana

## Zadanie 1 - Przygotowanie rozszerzonego zestawu testów jednostowych


**Cel:** Celem zadania jest stworzenie pełnego - rozszerzonego scenariusza testów jednostkowych dla jednej wybranej klasy obiektów. Zakres testów powinien zawierać:

- Testy poprawnych danych 
- Testy niepoprawnych danych
- Testy związane z próbą wstrzyknięcia kodu `SQL` i kodu `JavaScript`
- Testy ekstremalne

**celem zadania jest przygotowanego zestawu testów - nie musisz poprawić definicji klasy tak, aby weryfikować wszystkie założenia — jeśli np. test niepoprawnych danych się nie uda (w sensie obiekt stworzy się mimo niepoprawnych daych) - to dalej jest ok. Test w takim wypadku ma się nie udać**

### Instrukcja:
1. **Wybór aplilacji**
   Zadanie można zrealizować w jednym z dwóch wybranych wariantów: Java lub Python. Obydwa warianty zostały zawarte w katalogach:
```shell
Java/
Python/
```
2.  **Wybór klasy/obiektu do realizacji testów**
    Wybierz, na którym obiekcie chcesz zrealizować testy - wystarczy stworzenie scenariusza testów dla jednego obiektu np. `com.example.thymeleaf.entity.Student` lub `project/book/models.py`
3. **Przygotowanie testów**
    referencja - slajdy od 40 z prezentacji o nazwie `5 6 7 SbD Kod.pdf`
4. **Zmodyfikowanie pliku `Dockerfile`**
    tak aby przed zbudowaniem obrazu zrealizowane zostały testy — w przypadku niepowodzenia testów operacja `docker build...` powinna być zakończona niepowodzeniem

## Zadanie 2 - JWT — wykorzystanie podatności oraz realizacja poprawki

**Cel:** celem zadania jest zweryfikowanie i zidentyfikowanie podatności w module uwierzytelnienia aplikacji, realizowanego na podstawie wystawiane przez aplikacje tokeny `JWT`. Do realizacji będzie atak polegający na próbie zalogowania się na konto administratora. Po poprawnie zrealizowanym ataku należy znaleźć błąd w aplikacji, a następnie go usunąć.

### Instrukcja:

1. **Przejdź do katalogu z aplikacją**
```shell
cd JWT
```
2. **Uruchom aplikacje**
```shell
docker build -t jwt --platform linux/amd64 .
docker run -it -p 443:443 jwt
```

Aplikacja będzie dostępna pod adresem `https://127.0.0.1:443`, aplikacja nie zawiera graficznego interfejsu użytkownika zawiera jedynie `API`
3. **Uruchom Postmana i zaimportowanie dostarczonej kolekcji**
Import kolekcji:
![test](.github/image2.png)

Po wskazaniu ścieżki do pliku `JWT-attacks.postman_collection.json`, wczytana zostanie kolekcja. W postmanie powinna ona wyglądać tak jak na screenie poniżej:

![img.png](.github/img3.png)

4. **Wykonaj atak na JWT, zaloguj się na użytkownika o nazwie `administrator`**

Zaimportowana przed chwilą kolekcja `Postmanowa`, zawiera kilka typów ataków i testów. Interesuje nas tylko katalog `none`. który podświetlony jest na powyższym screenie.

Aby przeprowadzić atak:
- Napierw wyślij request o nazwie `none-obtain-token`, w wyniku tej operacji otrzymasz odpowiedź, która zawiera wygenerowany token. Ten token wygenerowany został dla użytkownika o nazwie `Bob`
![img.png](.github/img4.png)
- Następnie otwórz request, o nazwie `none-send-token`, otwórz zakładkę `Body` a następnie w wartości parametru `jwt_token` umieść zmodyfikowany token. W przypadku niepoprawnego tokena otrzymasz widok jak poniżej. W przypadku przeklenienia tokena z poprzedniego żądania otrzymasz wartosć tokenu dla użytkownika o nazwie `Bob`
![img.png](.github/img5.png)
- Testuj te API tak długo aż otrzymasz odpowiedź, która będzie zbliżona do
![img.png](.github/img6.png)

**Podpowiedź**: podobny scenariusz był poruszany na wykładzie 8. 
**Podpowiedź 2**: Konkretne elementy tokena JWT, rozdzielane `.` są kodowane z wykorzystaniem base64 i mogą być edytowane niezależnie od siebie  
**Podpowiedź 3**: Nawet jeśli, któryś elementów tokena JWT jest usuwany, wiele bibliotek wymaga aby `.` był ostatni

Zachowaj zarówno wygenerowany token JWT jak i screen z odpowiedzią od API, który zaczynać będzie się od: `"message": "Congrats!! You've solved the JWT challenge!!",`

5. **Przygotuj poprawkę**

Podatność znajduję się w `JWT/jwt-signature-apis-challanges/app.json` w metodzie w linijce `22`. Usunięcie problemu jest dość prostę i polega na usunięciu dosłownie kilku symboli.

Wykonaj zmianę, a potem zweryfikuj czy działa ona w oczekiwany sposób
```shell
docker build -t jwt --platform linux/amd64 .
docker run -it -p 443:443 jwt
```


# Punktowanie (ćwiczenie oceniane w skali 0-5 pkt):
- 2 za zadanie 1
- 2 punty za wtkorzystanie podatnosci związanej z `JWT`
- 1 Punkt za propozycje usunięcia podatności

## Credits
* Java application - [GitHub Repo](https://github.com/pedrohenriquelacombe/spring-thymeleaf-crud-example)
* Python application - [GitHub Repo](https://github.com/MohammadSatel/Flask_Book_Library)
* JWT application - [GitHub Repo](https://github.com/onsecru/jwt-hacking-challenges)
* 
