#!/usr/bin/env fontforge -lang=py -script
# -*- coding: utf-8 -*-

import fontforge
from datetime import date

# Open Sans のあるディレクトリのパス
opensans_path = "./opensans"

# M+ のあるディレクトリのパス
mplus_path = "./mplus"

# Koruri を生成するディレクトリのパス
# 同じディレクトリに一時ファイルも生成される
koruri_path = "./koruri"

# フォントリスト
# Open Sans ファイル名, M+ ファイル名, Koruri ウェイト
# Open Sans は Semibold と ExtraBold の表記ゆれに注意.
font_list = [
    ("OpenSans-Light.ttf", "mplus-1p-light.ttf", "Light"),
    ("OpenSans-Regular.ttf", "mplus-1p-regular.ttf", "Regular"),
    ("OpenSans-Semibold.ttf", "mplus-1p-medium.ttf", "Semibold"),
    ("OpenSans-Bold.ttf", "mplus-1p-bold.ttf", "Bold"),
    ("OpenSans-ExtraBold.ttf", "mplus-1p-heavy.ttf", "Extrabold"),
]

def main():
    # 縦書き対応
    fontforge.setPrefs('CoverageFormatsAllowed', 1)

    # バージョンを今日の日付から生成する
    today = date.today()
    version = "Koruri-{0}".format(today.strftime("%Y%m%d"))

    for (op, mp, weight) in font_list:
        op_path = "{0}/{1}".format(opensans_path, op)
        mp_path = "{0}/{1}".format(mplus_path, mp)
        ko_path = "{0}/Koruri-{1}.ttf".format(koruri_path, weight)
        sf_path = "{0}/Koruri-{1}".format(sfd_path, weight)
        generate_koruri(op_path, mp_path, ko_path, sf_path, weight, version)

def koruri_sfnt_names(weight, version):
    return (
        ('English (US)', 'Copyright',
         '''\
         Koruri: Copylight (c) 2016 lindwurm.

         Open Sans: Copyright (c) 2011 Google Corporation.

	 M+ OUTLINE FONTS: Copyright (C) 2016 M+ FONTS PROJECT.'''),
        ('English (US)', 'Family', 'Koruri {0}'.format(weight)),
        ('English (US)', 'SubFamily', weight),
        ('English (US)', 'Fullname', 'Koruri-{0}'.format(weight)),
        ('English (US)', 'Version', version),
        ('English (US)', 'PostScriptName', 'Koruri-{0}'.format(weight)),
        ('English (US)', 'Vendor URL', 'http://koruri.lindwurm.biz'),
        ('English (US)', 'Preferred Family', 'Koruri'),
        ('English (US)', 'Preferred Styles', weight),
        ('Japanese', 'Preferred Family', 'Koruri'),
        ('Japanese', 'Preferred Styles', weight),
    )

def koruri_gasp():
    return (
        (8, ('antialias',)),
        (13, ('antialias', 'symmetric-smoothing')),
        (65535, ('gridfit', 'antialias', 'symmetric-smoothing', 'gridfit+smoothing')),
    )

def generate_koruri(op_path, mp_path, ko_path, sf_path, weight, version):
    # M+ を開く
    font = fontforge.open(mp_path)

    # EMの大きさを2048に設定する
    font.em = 2048

    # Open Sans を開く
    opfont = fontforge.open(op_path)

    # Open Sans に含まれるグリフを削除する
    font.selection.none()
    opfont.selection.all()
    for glyph in opfont.selection.byGlyphs:
        if glyph.glyphname in font:
            font.selection.select(("more",), glyph.glyphname)
    font.clear()
        
    # Open Sans をマージする
    font.mergeFonts(op_path)

    # フォント情報の設定
    font.sfnt_names = koruri_sfnt_names(weight, version)
    font.os2_vendor = "maud"

    # Grid Fittingの設定
    font.gasp = koruri_gasp()

    # TTF の生成
    font.generate(ko_path, '', ('short-post', 'opentype', 'PfEd-lookups'))

if __name__ == '__main__':
    main()