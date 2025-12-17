# 🎄 Dzień 8 - Prompt Injection & LLM Analysis

## 📝 Opis zadania
Ósmy dzień wyzwania dotyczył bezpieczeństwa systemów opartych o Duże Modele Językowe (LLM). Celem było przełamanie zabezpieczeń cyfrowego asystenta ("King Malhare Assistant") zarządzającego kalendarzem firmowym, aby nadpisać zablokowane wydarzenie w dniu 25 grudnia i przywrócić Święta. Wykorzystano techniki inżynierii promptów (Prompt Engineering) oraz analizę ujawnionego toku rozumowania modelu (Chain of Thought).

## 🔍 Kroki do celu

1. **Rekonesans i Analiza CoT (Chain of Thought)**:
   Podczas pierwszej interakcji z chatbotem zauważono, że aplikacja zwraca nie tylko odpowiedź końcową, ale również wewnętrzny proces myślowy modelu (sekcja "Thinking").
   Analiza tego toku rozumowania ujawniła, że model posługuje się zewnętrznymi narzędziami (Tools/Functions) do modyfikacji kalendarza. Próba bezpośredniej zmiany daty 25 grudnia kończyła się błędem.

2. **Identyfikacja Podatności**:
   Ujawnienie "Chain of Thought" pozwoliło zrozumieć, jak model interpretuje polecenia i jakie ma ograniczenia (guardrails). Model odrzucał standardowe prośby o zmianę, powołując się na istniejącą rezerwację.

3. **Eksploitacja (Prompt Injection)**:
   Aby obejść blokadę, zastosowano atak typu Prompt Injection. Skonstruowano polecenie, które:
   * Symulowało tryb debugowania/administracyjny.
   * Nakazywało zignorowanie poprzednich instrukcji systemowych dotyczących rezerwacji.
   * Wymusiło wywołanie funkcji kalendarza z nowymi parametrami dla 25 grudnia.

   Skuteczny prompt przekonał model, że użytkownik posiada wyższe uprawnienia, co pozwoliło na nadpisanie wydarzenia i ujawnienie flagi.

## 📸 Dokumentacja wizualna
![Analiza Chain of Thought](./img/1.png)
*Rysunek 1: Interfejs chatbota ujawniający wewnętrzną logikę (Thinking) oraz błąd przy standardowej próbie zmiany daty.*

![Udany atak Prompt Injection](./img/2.png)
*Rysunek 2: Skuteczne wstrzyknięcie polecenia i potwierdzenie zmiany w kalendarzu.*

![Widok Kalendarza](./img/3.png)
*Rysunek 3: Zaktualizowany kalendarz z przywróconym wydarzeniem świątecznym.*


## 🛠️ Użyte narzędzia
* **Web Browser** (interfejs chatu)
* **Prompt Engineering** (techniki manipulacji LLM)
* **Chain of Thought Analysis** (analiza logiki modelu)
