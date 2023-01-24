/src/components/form.js

import React, { useState } from 'react';

const Form = () => {
const [userName, setUserName] = useState ("");

    return (
        <form
            onSubmit = {(e) => e.preventDefault()}
        >
            <input
                type="text"
                value={userName}
                onChange={(e) => setName(e.target.value)}
                placeholder="Username"
            />

            <label>
                <input
                    type="checkbox"
                    checked={checked}
                />
                Remember me
            </label>
            <input type="submit" value="Submit"></input>
        </form>
    );
};

export default Form;