; Auto-generated. Do not edit!


(cl:in-package f1tenth_simulator-msg)


;//! \htmlinclude detected_drowsy.msg.html

(cl:defclass <detected_drowsy> (roslisp-msg-protocol:ros-message)
  ((detected_msg
    :reader detected_msg
    :initarg :detected_msg
    :type cl:integer
    :initform 0))
)

(cl:defclass detected_drowsy (<detected_drowsy>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <detected_drowsy>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'detected_drowsy)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name f1tenth_simulator-msg:<detected_drowsy> is deprecated: use f1tenth_simulator-msg:detected_drowsy instead.")))

(cl:ensure-generic-function 'detected_msg-val :lambda-list '(m))
(cl:defmethod detected_msg-val ((m <detected_drowsy>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader f1tenth_simulator-msg:detected_msg-val is deprecated.  Use f1tenth_simulator-msg:detected_msg instead.")
  (detected_msg m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <detected_drowsy>) ostream)
  "Serializes a message object of type '<detected_drowsy>"
  (cl:let* ((signed (cl:slot-value msg 'detected_msg)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <detected_drowsy>) istream)
  "Deserializes a message object of type '<detected_drowsy>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'detected_msg) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<detected_drowsy>)))
  "Returns string type for a message object of type '<detected_drowsy>"
  "f1tenth_simulator/detected_drowsy")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'detected_drowsy)))
  "Returns string type for a message object of type 'detected_drowsy"
  "f1tenth_simulator/detected_drowsy")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<detected_drowsy>)))
  "Returns md5sum for a message object of type '<detected_drowsy>"
  "ff98c70f36496c6ca8cfca46ed611646")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'detected_drowsy)))
  "Returns md5sum for a message object of type 'detected_drowsy"
  "ff98c70f36496c6ca8cfca46ed611646")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<detected_drowsy>)))
  "Returns full string definition for message of type '<detected_drowsy>"
  (cl:format cl:nil "int32 detected_msg~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'detected_drowsy)))
  "Returns full string definition for message of type 'detected_drowsy"
  (cl:format cl:nil "int32 detected_msg~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <detected_drowsy>))
  (cl:+ 0
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <detected_drowsy>))
  "Converts a ROS message object to a list"
  (cl:list 'detected_drowsy
    (cl:cons ':detected_msg (detected_msg msg))
))
