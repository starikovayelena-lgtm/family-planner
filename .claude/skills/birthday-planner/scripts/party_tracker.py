#!/usr/bin/env python3
"""Birthday party tracker: event facts, guests (RSVP/allergies/gifts), wishlist, thank-yous.

Standard library only. Data lives in one folder per party:
  event.json     child, age, date, time, address, area, rsvp_by, host, phone, theme
  guests.csv     name, parent, phone, rsvp, allergies, pickup, gift, thanked, notes
  wishlist.csv   item, price_sek, link, claimed_by, bought

Examples:
  party_tracker.py init --dir birthdays/sofia-2026 --child Sofia --age 7 --date 2026-11-14 \
      --time "14.00-16.00" --address "[adress]" --rsvp-by 2026-11-09 --host Yelena --phone "[telefon]"
  party_tracker.py add-guests --dir D --names "Elsa, Maja"
  party_tracker.py set --dir D --name Elsa --rsvp yes --allergies nötter --gift "det fina Stitch-gosedjuret"
    (write --gift so it reads after "blev så glad för ...", i.e. with article/definite form)
  party_tracker.py status --dir D
  party_tracker.py table --dir D --view gifts --format whatsapp
  party_tracker.py thankyou --dir D
  party_tracker.py wish-add --dir D --item "LEGO Stitch" --price 450
  party_tracker.py wish-claim --dir D --item "LEGO Stitch" --by Mormor
"""
import argparse
import csv
import datetime as dt
import json
import sys
from pathlib import Path

GUEST_FIELDS = ["name", "parent", "phone", "rsvp", "allergies", "pickup", "gift", "thanked", "notes"]
WISH_FIELDS = ["item", "price_sek", "link", "claimed_by", "bought"]
RSVP_VALUES = {"yes", "no", "pending"}
SV_WEEKDAYS = ["måndag", "tisdag", "onsdag", "torsdag", "fredag", "lördag", "söndag"]
SV_MONTHS = ["januari", "februari", "mars", "april", "maj", "juni", "juli",
             "augusti", "september", "oktober", "november", "december"]


def fail(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def sv_date(iso):
    """'2026-11-14' -> 'lördag 14 november'. Weekday computed, never guessed."""
    try:
        d = dt.date.fromisoformat(iso)
    except (TypeError, ValueError):
        return iso or ""
    return f"{SV_WEEKDAYS[d.weekday()]} {d.day} {SV_MONTHS[d.month - 1]}"


def genitive(name):
    """Swedish possessive: Sofia -> Sofias, Agnes -> Agnes, Max -> Max."""
    return name if name[-1:].lower() in ("s", "x", "z") else name + "s"


def read_csv(path, fields):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:  # tolerate older files missing a column
        for k in fields:
            r.setdefault(k, "")
    return rows


def write_csv(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def load_event(d):
    p = d / "event.json"
    if not p.exists():
        fail(f"No event.json in {d}. Run 'init' first.")
    return json.loads(p.read_text(encoding="utf-8"))


def find(rows, key, value, what):
    v = value.strip().lower()
    hits = [r for r in rows if r[key].strip().lower() == v]
    if not hits:
        names = ", ".join(r[key] for r in rows) or "(none yet)"
        fail(f"{what} '{value}' not found. Existing: {names}")
    return hits[0]


def cmd_init(a):
    d = Path(a.dir)
    d.mkdir(parents=True, exist_ok=True)
    try:
        dt.date.fromisoformat(a.date)
        if a.rsvp_by:
            dt.date.fromisoformat(a.rsvp_by)
    except ValueError:
        fail("Dates must be YYYY-MM-DD, e.g. 2026-11-14")
    event = {k: getattr(a, k) for k in
             ["child", "age", "date", "time", "address", "area", "rsvp_by", "host", "phone", "theme"]}
    p = d / "event.json"
    if p.exists():
        old = json.loads(p.read_text(encoding="utf-8"))
        old.update({k: v for k, v in event.items() if v not in (None, "")})
        event = old
    p.write_text(json.dumps(event, ensure_ascii=False, indent=2), encoding="utf-8")
    for name, fields in [("guests.csv", GUEST_FIELDS), ("wishlist.csv", WISH_FIELDS)]:
        if not (d / name).exists():
            write_csv(d / name, fields, [])
    print(f"Event saved in {d}: {event['child']} turns {event['age']}, kalas "
          f"{sv_date(event['date'])} kl. {event.get('time') or '?'}; "
          f"OSA {sv_date(event.get('rsvp_by')) or '?'}")
    days = (dt.date.fromisoformat(event["date"]) - dt.date.today()).days
    print(f"Days until kalas: {days}" + ("  -> SHORT-NOTICE MODE" if days < 14 else ""))


def cmd_add_guests(a):
    d = Path(a.dir)
    load_event(d)
    rows = read_csv(d / "guests.csv", GUEST_FIELDS)
    existing = {r["name"].strip().lower() for r in rows}
    added = []
    for n in [x.strip() for x in a.names.replace("\n", ",").split(",") if x.strip()]:
        if n.lower() in existing:
            continue
        rows.append({**{k: "" for k in GUEST_FIELDS}, "name": n, "rsvp": "pending", "thanked": "no"})
        existing.add(n.lower())
        added.append(n)
    write_csv(d / "guests.csv", GUEST_FIELDS, rows)
    print(f"Added {len(added)}: {', '.join(added) or '-'} (total {len(rows)})")


def cmd_set(a):
    d = Path(a.dir)
    rows = read_csv(d / "guests.csv", GUEST_FIELDS)
    r = find(rows, "name", a.name, "Guest")
    changes = {k: getattr(a, k) for k in GUEST_FIELDS[1:] if getattr(a, k, None) is not None}
    if "rsvp" in changes and changes["rsvp"] not in RSVP_VALUES:
        fail(f"--rsvp must be one of {sorted(RSVP_VALUES)}")
    if not changes:
        fail("Nothing to set. Use e.g. --rsvp yes --allergies nötter --gift 'bok'")
    r.update(changes)
    write_csv(d / "guests.csv", GUEST_FIELDS, rows)
    print(f"{r['name']}: " + ", ".join(f"{k}={v}" for k, v in changes.items()))


def cmd_status(a):
    d = Path(a.dir)
    ev = load_event(d)
    rows = read_csv(d / "guests.csv", GUEST_FIELDS)
    by = {v: [r["name"] for r in rows if r["rsvp"] == v] for v in ("yes", "no", "pending")}
    print(f"{ev['child']} {ev['age']} år — {sv_date(ev['date'])} kl. {ev.get('time') or '?'} — "
          f"OSA {sv_date(ev.get('rsvp_by')) or '?'}")
    print(f"Invited {len(rows)} | yes {len(by['yes'])} | no {len(by['no'])} | pending {len(by['pending'])}")
    if by["pending"]:
        print("Pending (send reminder): " + ", ".join(by["pending"]))
    allergies = [f"{r['name']} ({r['allergies']})" for r in rows if r["allergies"] and r["rsvp"] != "no"]
    print("Allergies: " + (", ".join(allergies) if allergies else "none reported"))
    missing = [k for k in ("address", "phone") if not ev.get(k) or ev[k].startswith("[")]
    if missing:
        print("To fill in: " + ", ".join(missing))
    n = len(by["yes"]) + len(by["pending"])  # plan for everyone who may still come
    if n:
        print(f"Food for {n} kids (+20%): ~{round(n * 2 * 1.2)} hot dogs OR ~{round(n * 3 * 1.2)} pizza slices; "
              f"~{round(n * 0.3, 1)} L drink; goodie bags: {n + 2} (incl. extra + sibling)")


def guests_table(rows, fmt):
    cols = ["name", "parent", "rsvp", "allergies", "gift", "thanked"]
    if fmt == "markdown":
        out = ["| Gäst | Förälder | OSA | Allergi | Present | Tackat |", "|---|---|---|---|---|---|"]
        out += ["| " + " | ".join(r[c] or "–" for c in cols) + " |" for r in rows]
        return "\n".join(out)
    icon = {"yes": "✅", "no": "❌", "pending": "⏳"}
    return "\n".join(f"- *{r['name']}* {icon.get(r['rsvp'], '')}" +
                     (f" – allergi: {r['allergies']}" if r["allergies"] else "") for r in rows)


def gifts_table(rows, fmt):
    rows = [r for r in rows if r["rsvp"] != "no"]
    if fmt == "markdown":
        out = ["| Gäst | Förälder | Present | Tack skickat |", "|---|---|---|---|"]
        out += [f"| {r['name']} | {r['parent'] or '–'} | {r['gift'] or '❓ okänd'} | "
                f"{'✅' if r['thanked'] == 'yes' else '–'} |" for r in rows]
        return "\n".join(out)
    return "\n".join(f"- *{r['name']}*: {r['gift'] or '❓'}" + (" ✅" if r["thanked"] == "yes" else "")
                     for r in rows)


def wishlist_table(rows, fmt):
    if fmt == "markdown":
        out = ["| Önskan | Pris (kr) | Tas av | Köpt |", "|---|---|---|---|"]
        out += [f"| {r['item']} | {r['price_sek'] or '–'} | {r['claimed_by'] or 'ledig'} | "
                f"{'✅' if r['bought'] == 'yes' else '–'} |" for r in rows]
        return "\n".join(out)
    return "\n".join(
        (f"- ~{r['item']}~ ({r['claimed_by']})" if r["claimed_by"] else f"- {r['item']}") +
        (f" ca {r['price_sek']} kr" if r["price_sek"] and not r["claimed_by"] else "") +
        (f" {r['link']}" if r["link"] and not r["claimed_by"] else "") for r in rows)


def cmd_table(a):
    d = Path(a.dir)
    if a.view == "wishlist":
        rows = read_csv(d / "wishlist.csv", WISH_FIELDS)
        print(wishlist_table(rows, a.format) if rows else "(wishlist empty — use wish-add)")
        return
    rows = read_csv(d / "guests.csv", GUEST_FIELDS)
    if not rows:
        print("(no guests yet — use add-guests)")
        return
    print((gifts_table if a.view == "gifts" else guests_table)(rows, a.format))


def cmd_thankyou(a):
    d = Path(a.dir)
    ev = load_event(d)
    rows = read_csv(d / "guests.csv", GUEST_FIELDS)
    todo = [r for r in rows if r["rsvp"] == "yes" and r["thanked"] != "yes"]
    unknown = [r["name"] for r in todo if not r["gift"]]
    child, host = ev["child"], ev.get("host") or ""
    for r in todo:
        hello = f"Hej {r['parent']}!" if r["parent"] else "Hej!"
        gift = (f" {child} blev så glad för {r['gift']} 🎁" if r["gift"]
                else f" Och tack för den fina presenten 🎁")
        print(f"--- {r['name']}" + (f" ({r['phone']})" if r["phone"] else ""))
        print(f"{hello} Stort tack för att {r['name']} kom på {genitive(child)} kalas 💙{gift} Kram {host}\n")
    if unknown:
        print("NOTE: gift unknown for: " + ", ".join(unknown) +
              " — ask Yelena, then run: set --name X --gift '...'")
    if not todo:
        print("Nothing to send: no confirmed guests without thanked=yes.")
    print("After sending, mark each: set --name X --thanked yes")


def cmd_wish_add(a):
    d = Path(a.dir)
    rows = read_csv(d / "wishlist.csv", WISH_FIELDS)
    rows.append({"item": a.item, "price_sek": a.price or "", "link": a.link or "",
                 "claimed_by": "", "bought": "no"})
    write_csv(d / "wishlist.csv", WISH_FIELDS, rows)
    print(f"Wishlist: {len(rows)} items")


def cmd_wish_claim(a):
    d = Path(a.dir)
    rows = read_csv(d / "wishlist.csv", WISH_FIELDS)
    r = find(rows, "item", a.item, "Wish")
    if r["claimed_by"] and r["claimed_by"].lower() != a.by.lower() and not a.force:
        fail(f"'{r['item']}' is already claimed by {r['claimed_by']}. Use --force to override.")
    r["claimed_by"] = a.by
    if a.bought:
        r["bought"] = "yes"
    write_csv(d / "wishlist.csv", WISH_FIELDS, rows)
    print(f"{r['item']} -> {a.by}" + (" (bought)" if a.bought else ""))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init", help="create or update the event")
    for k in ["dir", "child", "age", "date"]:
        s.add_argument(f"--{k}", required=True)
    for k in ["time", "address", "area", "rsvp-by", "host", "phone", "theme"]:
        s.add_argument(f"--{k}", default="")
    s.set_defaults(f=cmd_init)

    s = sub.add_parser("add-guests", help="add comma-separated guest names")
    s.add_argument("--dir", required=True); s.add_argument("--names", required=True)
    s.set_defaults(f=cmd_add_guests)

    s = sub.add_parser("set", help="update one guest's fields")
    s.add_argument("--dir", required=True); s.add_argument("--name", required=True)
    for k in GUEST_FIELDS[1:]:
        s.add_argument(f"--{k}")
    s.set_defaults(f=cmd_set)

    s = sub.add_parser("status", help="RSVP summary, allergies, food quantities")
    s.add_argument("--dir", required=True); s.set_defaults(f=cmd_status)

    s = sub.add_parser("table", help="guests/gifts/wishlist as markdown or WhatsApp text")
    s.add_argument("--dir", required=True)
    s.add_argument("--view", choices=["guests", "gifts", "wishlist"], default="guests")
    s.add_argument("--format", choices=["markdown", "whatsapp"], default="markdown")
    s.set_defaults(f=cmd_table)

    s = sub.add_parser("thankyou", help="Swedish thank-you message per confirmed guest")
    s.add_argument("--dir", required=True); s.set_defaults(f=cmd_thankyou)

    s = sub.add_parser("wish-add", help="add a wishlist item")
    s.add_argument("--dir", required=True); s.add_argument("--item", required=True)
    s.add_argument("--price"); s.add_argument("--link"); s.set_defaults(f=cmd_wish_add)

    s = sub.add_parser("wish-claim", help="mark who is buying a wishlist item")
    s.add_argument("--dir", required=True); s.add_argument("--item", required=True)
    s.add_argument("--by", required=True); s.add_argument("--bought", action="store_true")
    s.add_argument("--force", action="store_true"); s.set_defaults(f=cmd_wish_claim)

    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
