(define multiremberco
  (lambda (a lat col)
    (cond
      ((null? lat)
       (col (quote ()) (quote ())))
      ((eq? (car lat) a)
       (multiremberco a
                       (cdr lat)
                       (lambda (newlat seen)
                         (col newlat
                              (cons (car lat) seen)))))
      (else
        (multiremberco a
                        (cdr lat)
                        (lambda (newlat seen)
                          (col (cons (car lat) newlat)
                               seen)))))))

(define ls (quote (strawberries tuna and swordfish)))
(define last-friend 
 (lambda (x y) 
  (display x)
  (display y)
  (newline)
  (length x)))
(multirembrco (quote tuna) ls last-friend)
