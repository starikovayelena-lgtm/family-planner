# Canva invitation

## Steps
1. **Facts from the tracker:** read `event.json` (child, age, date, weekday, time, address, RSVP date, host phone). Re-verify the weekday by running code.
2. **Approve the text first.** Show Yelena the Swedish invitation text (template below) and fix anything she changes. It's quicker to fix text before the design exists.
3. **Create the design** with the Canva connector's `Canva:create-design` tool. Pass a `brief` like the one below and **omit `format`** so Canva picks the invitation size. If no widget appears, poll `Canva:get-create-design-async-job` with the returned `job_id` and `continuation_token` until it's done. Wait the `polling_policy.wait_seconds` the response gives between polls; polling sooner returns `polled_too_early`. If a plain `sleep` is blocked, use `python3 -c "import time; time.sleep(N)"`.
   - If `create-design` isn't available: use `Canva:generate-design` with `design_type: "invitation"`, show the candidates, then `Canva:create-design-from-candidate` for the one Yelena picks.
   - If Canva isn't connected: give the text and 3 Canva template search terms (e.g. "barnkalas inbjudan Stitch", "birthday invitation tropical kids"), and suggest connecting Canva in claude.ai settings.
4. **Verify (feedback loop).** Read the text back with `Canva:read-design` (design ID from the result) and compare it with the facts: name, age, weekday + date, time, address, RSVP date, phone, and å/ä/ö. If anything is off, say exactly what and fix it (edit in Canva, or regenerate with the corrected brief). Repeat until it matches. Extracted text can join words at line breaks ("Välkommenpå"); that's layout, not a typo. The preview thumbnail is sometimes blank, so tell Yelena to glance at the artwork in Canva before sending.
5. **Approval → email.** Yelena reviews the design in Canva and says **"approve"**. Then export it with `Canva:export-design` as **PNG** and email it to her own address (starikovayelena@gmail.com) with the Gmail connector. Subject: `Inbjudan: [Barn]s kalas [datum]`. Attach the PNG if the file can be downloaded (needs `export-download.canva.com` allowed); otherwise send the export download link (it expires after a few hours, so say so) plus the permanent Canva link. Include the ready-to-paste WhatsApp class-group text in the same email. Before exporting, re-read the design: Yelena may have edited it in Canva, so check the photo position and that no text is covered or missing. Never email anyone else without being asked.
6. **Share** the Canva link. Offer an export: `Canva:export-design` as **PNG** for WhatsApp (phone-friendly portrait), or **PDF** to print and hand out.

## Photo of the birthday child
Use the photo exactly as Yelena provides it (she prefers the full picture, not a crop). Upload it with `Canva:create-upload-url` (POST the raw bytes; this needs `www.canva.com` allowed in the session's network settings). Then add it with `Canva:edit-design` `insert_fill` in the space between the age line and the date, and move the text below it down. If the upload is blocked, give Yelena the cropped file and tell her to drag it into the design in Canva.

## Brief template
```
Portrait children's birthday party invitation for a [age]-year-old girl, to share as an image in WhatsApp.
Theme: [theme] — [colours / imagery from the theme pack]. Playful, bright, easy to read on a phone.
Use exactly this Swedish text, keeping å/ä/ö:
"[Title line]
[Child] fyller [age] år!
[Weekday] [day] [month], kl. [time]
[Address]
OSA senast [weekday day month] till [host], [phone]
[Optional tagline — no dress-code request]"
Don't add any other dates, names, or text. Don't use copyrighted logos; theme-inspired artwork is fine.
```

## Swedish invitation text (default)
```
[Emoji] Välkommen på [tema]-kalas! [Emoji]

[Barn] fyller [ålder] år och vill fira med dig!

När:  [Veckodag] [dag] [månad], kl. [tid]
Var:  [adress]

OSA senast [veckodag dag månad] till [värd], [telefon].
Berätta gärna om ditt barn har någon allergi.

Varmt välkommen! / [Barn]
```
