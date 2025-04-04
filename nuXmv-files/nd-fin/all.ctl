EG(x > 1 | x < -1)
!(EG(x > 1 | x < -1))
AF(AG(x <= 1) & AG (x >= -1))

EG(AF(x = 0))
!(EG(AF(x = 0))
AF(AG(x <= 1) & AG (x >= -1))

EG(AF(x = 0))
!(EG(AF(x = 0)))

AG(a != 1 | AF(r = 1))
!(AG(a != 1 | AF(r = 1)))

EF(a = 1 & EG(r != 5))
!EF(a = 1 & EG(r != 5)))

AG(a != 1 | EF(r = 1))
!(AG(a != 1 | EF(r = 1)))

EF(a = 1 & AG(r != 1))
!(EF(a = 1 & AG(r != 1)))

AG(s != 1 | AF(u = 1))
!(AG(s != 1 | AF(u = 1)))

EF(s = 1 | EG(u != 1))
!(EF(s = 1 | EG(u != 1)))

AG(s != 1 | EF(u = 1))
!(AG(s != 1 | EF(u = 1)))

AG(AF(w >= 1))
!(AG(AF(w >= 1)))

EF(EG(w < 1))
!(EF(EG(w < 1)))

AG(EF(w >=1))
!(AG(EF(w >=1)))

EF(AG(w < 1))
!(EF(AG(w < 1)))

AG(AF(w = 1))
!(AG(AF(w = 1)))

EF(EG(w != 1))
!(EF(EG(w != 1)))

AG(EF(w = 1))
!(AG(EF(w = 1)))

EF(AG(w != 1))
!(EF(AG(w != 1)))

(c > 5) -> (AF(r > 5))
!((c > 5) -> (AF(r > 5)))

(c > 5) & EG(r <= 5)
!((c > 5) & EG(r <= 5))

(c <= 5) | EF(r > 5)
!((c <= 5) | EF(r > 5))

(c > 5) & AG(r <= 5)
!((c > 5) & AG(r <= 5))