---
name: birthday-planner
description: Plans birthdays for Yelena's daughters Sofia (9 Nov) and Amelia, every year, end to end. Covers the family celebration on the day, the Swedish kalas (at home or at a venue), a Canva invitation, WhatsApp messages in Swedish (invitation, RSVP reminder, practical info, thank-yous), a guest/RSVP/allergy tracker, a who-gave-what gift table, and wishlist coordination with relatives. Use whenever Yelena mentions a birthday, födelsedag, kalas, party, invitation, inbjudan, OSA, presents or gifts, wishlist, goodie bags, birthday cake, thank-you messages, or a child turning a new age, even if she doesn't say "plan".
---

# Birthday planner

The goal is to save Yelena hours. Reuse what is already known, ask only for what's missing, and produce ready-to-send outputs: a Canva invitation, WhatsApp text, and tables.

## Files: read when needed

| File | Read when |
|------|-----------|
| [references/family.md](references/family.md) | **Always, first.** Child profiles, birthdays, home, past-party log |
| [references/party-playbook.md](references/party-playbook.md) | Choosing a format, program, games, food, budget, countdown, day-of roles |
| [references/themes.md](references/themes.md) | A theme is chosen or needs suggesting |
| [references/canva-invitation.md](references/canva-invitation.md) | Making the invitation |
| [references/whatsapp-templates.md](references/whatsapp-templates.md) | Writing any message to parents, the class group, or relatives |
| `scripts/party_tracker.py` | Guests, RSVPs, allergies, gifts, wishlist, thank-you messages (run it; don't read it) |

## Workflow

Copy this checklist into the reply and tick items off as the birthday progresses. A request may start at any step, e.g. "write the thank-yous".

```
Birthday progress — [Child] turns [N] on [date]
- [ ] 1. Facts: age, weekday, days left, mode (normal / short notice)
- [ ] 2. Basics decided: kalas date+time, guest group, home/venue, theme
- [ ] 3. Guest list: Notion "Birthday party guests" (+ local tracker for texts)
- [ ] 4. Invitation: Swedish text approved → Canva design → "approve" → email PNG + WhatsApp text to Yelena
- [ ] 5. Plan: program, shopping list (amazon.se + local), budget, adult roles
- [ ] 6. Follow-ups: RSVP reminder, practical-info message, allergy check
- [ ] 7. After: who-gave-what table, thank-you messages
- [ ] 8. Log the year in references/family.md
```

**1. Facts.** Compute the age from the birth year, and get the weekday and days left by running code. Never compute weekdays mentally, because a wrong weekday on an invitation is the most common error:
`python3 -c "import datetime as d; x=d.date(2026,11,14); print(x.strftime('%A'), (x-d.date.today()).days)"`
Under 14 days to the kalas → **short-notice mode** (see the playbook).
**RSVP date:** about 8 days before the kalas (the same weekday the week before is easy to remember). In short-notice mode, use 5–6 days after the invitation goes out, but at least 5 days before the kalas. Never put it on the birthday itself. Note clashes such as school holidays, Fars dag/Mors dag, and the other daughter's activities.

**2. Basics.** Ask at most 4 questions, in one go, and only for what isn't in family.md: date and time, guest group (whole class / all girls / a few friends / family), home or venue, theme. Offer a recommended default for each.

**3. Guest list.** The shared guest list lives in Notion, so it survives between sessions and Alex can see it: the **Birthday party guests** database (https://app.notion.com/p/44f893186e8c40a0a4964fa8564fa3bc, data source `collection://2056eeef-3bed-41ec-8a68-fde72eed7077`).
- One database for every year. Each row is one guest; the `Party` select is "<Child> <Year>" (e.g. "Sofia 2026"). Add a new option for a new party with the Notion update-data-source tool, then create rows with `Notion:notion-create-pages` (parent = the data source). Columns: Guest, Party, RSVP (Pending/Yes/No), Parent, Phone, Allergies, Pickup, Gift, Thank-you sent, Notes.
- When Yelena reports RSVPs, allergies or gifts, update the rows. For headcounts and "who gave what", query rows filtered by Party.
- If Notion isn't connected, use the local tracker instead and offer the CSV.

The local tracker script still generates the Swedish texts (status, food quantities, thank-yous). Mirror the Notion rows into it when needed:
```bash
python3 scripts/party_tracker.py init --dir birthdays/sofia-2026 --child Sofia --age 6 --date 2026-11-14 --time "14.00-16.00" --address "[adress]" --area Skanör-Falsterbo --rsvp-by 2026-11-06 --host Yelena --phone "[telefon]"
python3 scripts/party_tracker.py add-guests --dir birthdays/sofia-2026 --names "Elsa, Maja, Alva"
python3 scripts/party_tracker.py set --dir birthdays/sofia-2026 --name Elsa --rsvp yes --allergies nuts --parent Anna
python3 scripts/party_tracker.py status --dir birthdays/sofia-2026
```
Run `python3 scripts/party_tracker.py --help` for all commands (`wish-add`, `wish-claim`, `table`, `thankyou`). The cloud session is temporary, so give Yelena the CSVs and offer to mirror them in a Google Sheet or Notion.

**4. Invitation.** Draft the Swedish text first and get Yelena's OK. If you can't ask (e.g. running as a subagent), go ahead with the draft and list the text under questions, since a Canva design is easy to edit. Then follow canva-invitation.md. Before sharing, **verify the design against `event.json`**: weekday + date, time, address, RSVP date, phone number, child's name and age, and å/ä/ö spelling. If anything is wrong, fix it and check again. Pair the image with the WhatsApp invitation template.
When Yelena says **"approve"**: re-read the design (she may have edited it), export a PNG, and email her both the image (or its download link) and the WhatsApp class-group text **as plain text** (no HTML), so she can copy and paste it on her phone. Also show the WhatsApp text in chat in a code block.

**5. Plan.** Use the playbook and theme pack. If the guest count is unknown, plan for the class size from family.md (otherwise 12), label it a default, and rescale once RSVPs arrive (`status` prints quantities). Output a timed program, a shopping list split into *amazon.se* (order ≥7 days ahead, give search terms) and *local/ICA*, food quantities from the guest count, a budget, and adult roles.
Put the actionable part in **Notion**: one private to-do page per party ("<Child> <age> år: <theme>-kalas to-do") with dated checkbox sections, decor/dress/gift checklists with amazon.se links, and links to the guest database, the Canva design and the GitHub plan. The full plan lives in `birthdays/<child>-<year>/plan.md` in the family-planner repo. Commit and push after changes.
Gifts and outfits don't have to match the theme: offer a mix (theme item + general age-appropriate ideas).

**6–7. Messages and gifts.** Use the WhatsApp templates. For the gift table and thank-yous, run `table --view gifts` and `thankyou`. Never invent who gave what; ask if a gift is unknown.

**8. Log the year.** Append a row to the log in family.md: theme, format, guest count, cost, what worked, and what to skip next year. Update the profile (interests, sizes, wishlist). Next year's planning starts from here.

## Gotchas

- **Never invent the address, phone numbers, children's names or gifts.** Use `[adress]`-style placeholders and list them as "to fill in".
- **WhatsApp renders no tables, headings or links in text.** Use the script's `--format whatsapp` output (bold names, `- ` lists). Markdown tables are for chat with Yelena or Notion only.
- **Canva AI designs can change details or mangle å/ä/ö.** Always check the preview text against the facts before calling it done.
- **Class norms:** post in the class WhatsApp group only when the whole class or the whole girls' group is invited. Otherwise send individual messages. Ask parents about allergies.
- **Venues, prices and opening hours change.** Verify with a web search and mark anything unverified.
- **The other sister:** give her a role (game leader, helper) and a goodie bag.
- **Photos:** ask other parents before posting pictures of their children.

## Output defaults

- Guest-facing text (invitations, WhatsApp) in **Swedish**. Talk to Yelena in English unless she writes in Swedish.
- Dates in Swedish style ("lördag 14 november, kl. 14.00–16.00"). Money in SEK.
- End each reply with the next 1–3 concrete actions and their dates.
