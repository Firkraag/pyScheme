(define (rember a lat)
  (cond
    ((null? lat) (quote ()))
    ((eq? (car lat) a) (cdr lat))
    (else
      (cons (car lat) (rember a (cdr lat))))
    ))
(define a (quote and))
(define lat (quote (bacon lettuce and tomato)))
(rember a lat)
(rember (quote and) lat)
(define lat (rember (quote lettuce) lat))
(rember (quote and) lat)
