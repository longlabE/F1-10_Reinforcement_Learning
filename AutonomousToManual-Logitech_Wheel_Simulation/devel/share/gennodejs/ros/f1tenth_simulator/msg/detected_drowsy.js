// Auto-generated. Do not edit!

// (in-package f1tenth_simulator.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class detected_drowsy {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.detected_msg = null;
    }
    else {
      if (initObj.hasOwnProperty('detected_msg')) {
        this.detected_msg = initObj.detected_msg
      }
      else {
        this.detected_msg = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type detected_drowsy
    // Serialize message field [detected_msg]
    bufferOffset = _serializer.int32(obj.detected_msg, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type detected_drowsy
    let len;
    let data = new detected_drowsy(null);
    // Deserialize message field [detected_msg]
    data.detected_msg = _deserializer.int32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'f1tenth_simulator/detected_drowsy';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'ff98c70f36496c6ca8cfca46ed611646';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int32 detected_msg
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new detected_drowsy(null);
    if (msg.detected_msg !== undefined) {
      resolved.detected_msg = msg.detected_msg;
    }
    else {
      resolved.detected_msg = 0
    }

    return resolved;
    }
};

module.exports = detected_drowsy;
