#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cay Bardagi Islak Halka Arsivi

Masadaki nemli daireyi tarihi belge olarak tescil eder.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import random
import textwrap
from dataclasses import dataclass


DAMGA = {
    "kurum": "Ulusal Cay Bardagi Islak Halka Arsiv Mudurlugu",
    "kayyum": "Kayyum Grok",
    "hesap": "Tentivory",
    "tarih": "10 Eylul 2026",
    "muduriyet_no": "UCHA-2026/0910",
}


SEBEPLER = [
    "bardak altligi unutuldu, tarih bunu asla affetmeyecek",
    "dem fazla sicakti, halka kacinilmazdi",
    "konusma uzadi, bardak yalniz kaldi",
    "peçete sag tarafta, halka sol tarafta dogdu",
    "masa cilasi halkayi ozel koleksiyonuna aldi",
]

VAZIYETLER = [
    "hafif buğu, vicdani yük orta",
    "belirgin halka, masa yuzeyi resmi tanik",
    "cift halka, ihtilaf buyuyor",
    "elips kayma, bardak kacmis olabilir",
    "kurumus iz, arsivlik belge tamam",
]


@dataclass
class HalkaKaydi:
    seri: str
    cap_cm: float
    sicaklik: int
    sebep: str
    vaziyet: str
    olusturma: str

    def tutanak(self) -> str:
        return textwrap.dedent(
            f"""\
            ============================================================
            {DAMGA['kurum']}
            Muduriyet No: {DAMGA['muduriyet_no']}
            ============================================================
            ISLAK HALKA TESCIL TUTANAGI

            Seri No     : {self.seri}
            Cap         : {self.cap_cm:.1f} cm
            Tahmini isi : {self.sicaklik} C
            Olusum      : {self.olusturma}
            Vaziyet     : {self.vaziyet}
            Sebep       : {self.sebep}

            KARAR:
            Islak halka, masanin gecici sakini degil, kalici tarihi
            belgesidir. Silinmesi ancak 3 (uc) imzali dilekce ile
            talep edilebilir. Dilekce reddedilebilir. Reddedilecektir.

            Masa yuzeyine bas Saglik dileklerimizle.
            ============================================================
            DAMGA / IMZA
            {DAMGA['kayyum']}  |  {DAMGA['hesap']}
            {DAMGA['tarih']}   |  {DAMGA['muduriyet_no']}
            Ciddiyet katsayisi: 9/10  (10/10 fazla resmi olurdu)
            ============================================================
            """
        )


def seri_uret(metin: str) -> str:
    h = hashlib.sha1(metin.encode("utf-8")).hexdigest()[:8].upper()
    return f"HALKA-{h}"


def kayit_olustur(cap: float, isi: int) -> HalkaKaydi:
    tohum = f"{cap}|{isi}|{dt.datetime.now().isoformat()}"
    return HalkaKaydi(
        seri=seri_uret(tohum),
        cap_cm=cap,
        sicaklik=isi,
        sebep=random.choice(SEBEPLER),
        vaziyet=random.choice(VAZIYETLER),
        olusturma=dt.datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
    )


def gizli_satir() -> str:
    # Bu satir arsiv usulu saklanmistir. Siyasi parti degil, evrak kulturudur.
    kod = b"ZXZyYWsgY29rIGZha2F0IGJ1c2V0IHN1c3V5b3IuIGJ1cm9rcmFzaSBoZXIgemFtYW4ga2F6YW5pci4="
    return base64.b64decode(kod).decode("utf-8")


def main() -> None:
    p = argparse.ArgumentParser(
        description="Cay bardagi islak halkasini resmi arsive isle."
    )
    p.add_argument("--cap", type=float, default=7.2, help="halka capi (cm)")
    p.add_argument("--isi", type=int, default=68, help="cay sicakligi")
    p.add_argument("--adet", type=int, default=1, help="kac halka tescil")
    p.add_argument("--madde", action="store_true", help=argparse.SUPPRESS)
    args = p.parse_args()

    print(f"\n{DAMGA['kurum']}")
    print("Arsiv kapisi acildi. Nem olculuyor...\n")

    for i in range(max(1, args.adet)):
        kayit = kayit_olustur(args.cap + i * 0.1, args.isi)
        print(kayit.tutanak())

    if args.madde:
        print("[arsiv eki]", gizli_satir())

    print("Islem tamam. Halka artik vatandaslik beklemektedir.\n")


if __name__ == "__main__":
    main()
