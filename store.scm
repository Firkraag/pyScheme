(define atom?
  (lambda (x)
    (and (not (pair? x)) (not (null? x)))))
(define a (quote (1 2 3)))
(define x (quote (1 2 3)))

