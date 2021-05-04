const mongoose = require('mongoose');

const usersSchema = mongoose.Schema({

    firstName: String,
    lastName: String,
    emailAddress: String,
    phoneNumber: String,
    dob: Date,
    zipCode: Number,
    School: String
});

const usersModel = mongoose.model('Users', usersSchema);

module.exports = usersModel;