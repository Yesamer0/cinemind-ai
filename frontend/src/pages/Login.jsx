import { useState } from "react";
import axios from "axios";

function Login() {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    async function handleLogin(e) {

        e.preventDefault();

        setError("");
        setLoading(true);

        try {

            const formData = new URLSearchParams();

            formData.append("username", username);
            formData.append("password", password);

            const response = await axios.post(
                "http://127.0.0.1:8000/login",
                formData,
                {
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                    }
                }
            );

            console.log("Login successful:", response.data);

            localStorage.setItem(
                "token",
                response.data.access_token
            );

            localStorage.setItem(
                "user",
                JSON.stringify({
                    id: response.data.user_id,
                    username: response.data.username
                })
            );

            alert("Login successful!");

        } catch (error) {

            console.error(error);

            setError(
                error.response?.data?.detail ||
                "Login failed."
            );

        } finally {

            setLoading(false);

        }
    }

    return (
        <div>

            <h1>Login</h1>

            <form onSubmit={handleLogin}>

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
                    {loading ? "Logging in..." : "Login"}
                </button>

            </form>

            {error && (
                <p>{error}</p>
            )}

        </div>
    );
}

export default Login;