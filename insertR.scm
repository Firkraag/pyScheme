(define insertR
  (lambda (new old lat)
    (cond
      ((null? lat) '())
      ((eq? (car lat) old) (cons old (cons new (cdr lat))))
      (else (cons (car lat)
                  (insertR new old (cdr lat)))))))
(define insertR*
  (lambda (new old l)
    (cond
      (null? '())
      ((atom? (car l))
       (cond
         ((eq? (car l) old) 
          (cons old (cons new (insertR* new old (cdr l)))))
         (else
           (cons (car l) (insertR* new old (cdr l))))))
      (else
        (cons (insertR* new old (car l)) 
              (insertR* new old (cdr l)))))))
