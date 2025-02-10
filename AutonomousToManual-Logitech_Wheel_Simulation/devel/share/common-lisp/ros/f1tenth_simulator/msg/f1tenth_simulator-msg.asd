
(cl:in-package :asdf)

(defsystem "f1tenth_simulator-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "detected_drowsy" :depends-on ("_package_detected_drowsy"))
    (:file "_package_detected_drowsy" :depends-on ("_package"))
  ))