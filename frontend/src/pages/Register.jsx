import { useState } from "react";
import axios from "axios";

function Register() {

    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    async function handleRegister(e) {

        e.preventDefault();

        setError("");
        setSuccess("");

        try {

            const response = await axios.post(
                "http://127.0.0.1:8000/register",
                null,
                {
                    params: {
                        username,
                        email,
                        password
                    }
                }
            );

            console.log("Register successful:", response.data);

            setSuccess("Registration successful!");

            setUsername("");
            setEmail("");
            setPassword("");

        } catch (error) {

            console.error(error);

            setError(
                error.response?.data?.detail ||
                "Registration failed."
            );
        }
    }

    return (
        <div>

            <h1>Register</h1>

            <form onSubmit={handleRegister}>

                <div>
                    <label>Username</label>

                    <input
                        type="text"
                        value={username}
                        onChange={(e) =>
                            setUsername(e.target.value)
                        }
                    />
                </div>

                <br />

                <div>
                    <label>Email</label>

                    <input
                        type="email"
                        value={email}
                        onChange={(e) =>
                            setEmail(e.target.value)
                        }
                    />
                </div>

                <br />

                <div>
                    <label>Password</label>

                    <input
                        type="password"
                        value={password}
                        onChange={(e) =>
                            setPassword(e.target.value)
                        }
                    />
                </div>

                <br />

                <button type="submit">
                    Register
                </button>

            </form>

            {success && (
                <p>{success}</p>
            )}

            {error && (
                <p>{error}</p>
            )}

        </div>
    );
}

export default Register;