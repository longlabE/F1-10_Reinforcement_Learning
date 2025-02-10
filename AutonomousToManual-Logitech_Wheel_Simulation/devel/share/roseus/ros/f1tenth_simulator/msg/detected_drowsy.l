;; Auto-generated. Do not edit!


(when (boundp 'f1tenth_simulator::detected_drowsy)
  (if (not (find-package "F1TENTH_SIMULATOR"))
    (make-package "F1TENTH_SIMULATOR"))
  (shadow 'detected_drowsy (find-package "F1TENTH_SIMULATOR")))
(unless (find-package "F1TENTH_SIMULATOR::DETECTED_DROWSY")
  (make-package "F1TENTH_SIMULATOR::DETECTED_DROWSY"))

(in-package "ROS")
;;//! \htmlinclude detected_drowsy.msg.html


(defclass f1tenth_simulator::detected_drowsy
  :super ros::object
  :slots (_detected_msg ))

(defmethod f1tenth_simulator::detected_drowsy
  (:init
   (&key
    ((:detected_msg __detected_msg) 0)
    )
   (send-super :init)
   (setq _detected_msg (round __detected_msg))
   self)
  (:detected_msg
   (&optional __detected_msg)
   (if __detected_msg (setq _detected_msg __detected_msg)) _detected_msg)
  (:serialization-length
   ()
   (+
    ;; int32 _detected_msg
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _detected_msg
       (write-long _detected_msg s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _detected_msg
     (setq _detected_msg (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get f1tenth_simulator::detected_drowsy :md5sum-) "ff98c70f36496c6ca8cfca46ed611646")
(setf (get f1tenth_simulator::detected_drowsy :datatype-) "f1tenth_simulator/detected_drowsy")
(setf (get f1tenth_simulator::detected_drowsy :definition-)
      "int32 detected_msg
")



(provide :f1tenth_simulator/detected_drowsy "ff98c70f36496c6ca8cfca46ed611646")


