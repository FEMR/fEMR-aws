import React, { useState } from "react";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import { FormControl, FormLabel } from "@mui/material";

function ContactForm() {
  const [submitted, setSubmitted] = useState(false);
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [organization, setOrganization] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (event) => {
    setSubmitted(true);
    event.preventDefault();
    console.log(
      `First Name: ${firstName}\nLast Name: ${lastName}\nEmail: ${email}\nOrganization: ${organization}\nMessage: ${message}`
    );
    // You can replace the console.log with your desired submit logic
    await fetch(
      "https://qetcdnt6vd.execute-api.us-east-2.amazonaws.com/prod/enroll",
      {
        method: "PUT",
        body: JSON.stringify({
          first_name: firstName,
          last_name: lastName,
          email: email,
          role: 1,
          organization: organization,
          message: message,
        }),
        headers: {
          "Content-Type": "application/json",
        },
      }
    )
      .then((response) => response.json())
      .then((data) => console.log(data))
      .catch((error) => console.error(error));

    setTimeout(() => {
      setSubmitted(false);
      setFirstName("");
      setLastName("");
      setEmail("");
      setOrganization("");
      setMessage("");
    }, 1000);
  };

  return (
    <div>
      <center>
        <h1>New User Enrollment Form</h1>
        <FormControl>
          {submitted && <p>Submitted!</p>}
          <FormLabel>First Name</FormLabel>
          <TextField
            type="text"
            value={firstName}
            onChange={(firstName) => setFirstName(firstName.target.value)}
          ></TextField>
          <FormLabel>Last Name</FormLabel>
          <TextField
            type="text"
            value={lastName}
            onChange={(lastName) => setLastName(lastName.target.value)}
          ></TextField>
          <FormLabel>Email</FormLabel>
          <TextField
            type="email"
            value={email}
            onChange={(email) => setEmail(email.target.value)}
          ></TextField>
          <FormLabel>Organization</FormLabel>
          <TextField
            type="text"
            value={organization}
            onChange={(organization) =>
              setOrganization(organization.target.value)
            }
          ></TextField>
          <FormLabel>Message</FormLabel>
          <TextField
            id="outlined-multiline-flexible"
            multiline
            maxRows={4}
            value={message}
            type="text"
            onChange={(message) => setMessage(message.target.value)}
          ></TextField>
          <Button onClick={handleSubmit}>Submit</Button>
        </FormControl>
      </center>
    </div>
  );
}

export default ContactForm;
