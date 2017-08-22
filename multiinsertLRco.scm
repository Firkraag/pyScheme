(define multiinsertLRco
  (lambda (new oldL oldR lat col)
    (cond
      ((null? lat)
       (col (quote ()) 0 0))
      ((eq? (car lat) oldL)
       (multiinsertLRco new oldL oldR
                        (cdr lat)
                        (lambda (newlat L R)
                          (col (cons new
                                     (cons oldL newlat))
                               (add1 L) R))))
      ((eq? (car lat) oldR)
       (multiinsertLRco new oldL oldR
                        (cdr lat)
                        (lambda (newlat L R)
                          (col (cons oldR (cons new newlat))
                          L (add1 R)))))
      (else
        (multiinsertLRco new oldL oldR
                         (cdr lat)
                         (lambda (newlat L R)
                           (col (cons (car lat) newlat)
                                L R)))))))

(define add1 (lambda (x) (+ x 1)))
(define col 
  (lambda (lat x y)
    (display x)
    (display y)
    (display lat)
    (newline)
    ))

(define newlat (quote (chips and fish or fish and chips)))
(multiinsertLRco (quote salt) (quote fish) (quote chips) newlat col)
