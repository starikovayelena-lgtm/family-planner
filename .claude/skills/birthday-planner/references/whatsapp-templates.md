# WhatsApp templates (Swedish)

## Formatting rules
WhatsApp supports `*bold*`, `_italic_`, `~strike~`, `- ` bullet lists, `1. ` numbered lists, and ``` monospace ```.
It does **not** render markdown headings, tables or `[text](links)`. Paste plain URLs.
Keep messages short enough to read on one phone screen. **Yelena likes fun, playful messages:** use plenty of emoji that match the theme (about 8–12 in an invitation, spread over the lines, not piled up at the end). For Stitch/Hawaii: 🌺🌴🏝️🐚🍍🥥🤙🌈👽💙🏄‍♀️, and greet with "Aloha" / sign off with "Mahalo". Other themes: pick 6–8 matching emoji (unicorn 🦄🌈✨🎀, horses 🐴🏆🌾, disco 🪩🎤💃✨, mermaid 🧜‍♀️🐚🌊💎).
Fill `{placeholders}` from the tracker's `event.json` (`{area}` = the `area` field, e.g. Skanör-Falsterbo). Leave `[brackets]` for anything unknown and tell Yelena.

## 1. Invitation: class group (send with the Canva image)
Approved Stitch/Hawaii example (2026), the style to follow:
```
🌺🌴 Aloha alla! 🌴🌺
Sofia fyller 6 år och vi har Stitch-kalas 💙👽 *lördag 14 november, kl. 14.00–16.00* hemma hos oss i Falsterbo 🏝️
Alla tjejer i klassen är välkomna! 🐚✨
Inbjudan finns i bilden ⬆️🎉
🍍 OSA senast *söndag 8 november* till mig, och berätta gärna om allergier 🥥
Mahalo och aloha! 🤙🌈
Yelena (Sofias mamma) 🌸
```
Generic version (add theme emoji as above):
```
Hej alla! 🎉
{child} fyller {age} år och vi har kalas *{weekday} {date}, kl. {time}* hemma hos oss i {area}. Alla tjejer i klassen är välkomna! 💙
Inbjudan finns i bilden ⬆️
OSA senast *{rsvp_by}* till mig, och berätta gärna om allergier.
Hälsningar {host} ({child}s mamma)
```
Change "Alla tjejer i klassen" to match the guest group. Post in the group only when the **whole** group is invited.

## 2. Invitation: individual message
```
Hej {parent}! {child} fyller {age} år och vill gärna bjuda {guest} på kalas *{weekday} {date}, kl. {time}* hos oss ({address}). 🎉
Inbjudan i bilden. OSA senast {rsvp_by}, och säg gärna till om {guest} har någon allergi. Hälsningar {host}
```

## 3. RSVP reminder (2 days before the deadline, only to those who haven't answered)
```
Hej {parent}! En liten påminnelse om {child}s kalas {weekday} {date} kl. {time} 😊 Kan {guest} komma? Svara gärna senast {rsvp_by}. Tack! /{host}
```

## 4. Practical info (the day before, to confirmed guests)
```
Hej! Vi ser fram emot imorgon 🎉
*{weekday} {date}, kl. {time}*
📍 {address} {parking_or_door_tip}
- Lämning {start}, hämtning *{end}*
- {theme_note}
- Allergier vi har noterat: {allergy_list}. Hör av er om något saknas!
Ring {phone} om något dyker upp. /{host}
```

## 5. Reply to "Vad önskar hon sig?"
```
Hej! Vad snällt 😊 {child} gillar {interests} just nu. Några tips:
- {wish_1}
- {wish_2}
- {wish_3}
Men ingen present behövs, det viktigaste är att {guest} kommer! 💙
```

## 6. Gift coordination with relatives (avoid duplicate presents)
Generate the list with `party_tracker.py table --view wishlist --format whatsapp`, then wrap it:
```
Hej allihop! Här är {child}s önskelista inför {age}-årsdagen 🎁
Skriv vad ni tar så vi inte köper samma sak:
{wishlist_whatsapp}
Kram {host}
```

## 7. Thank-yous to guests
Generate them with `party_tracker.py thankyou`. One message per family, naming the gift. Send within 1–3 days.

## 8. Thank-you to relatives
```
Hej {name}! Tusen tack för {gift} 💙 {child} blev jätteglad och {small_detail}. Kram från oss alla!
```
Ask Yelena for one small detail (e.g. "har sovit med den varje natt"). It makes the message feel personal.
