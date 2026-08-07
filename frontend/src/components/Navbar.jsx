import { Link, useNavigate } from "react-router-dom";

function Navbar() {

    const navigate = useNavigate();

    const token = localStorage.getItem("token");
    const user = JSON.parse(localStorage.getItem("user"));

    function handleLogout() {

        localStorage.removeItem("token");
        localStorage.removeItem("user");

        navigate("/login");
    }

    return (
        <nav
            style={{
                padding: "15px",
                borderBottom: "1px solid gray",
                marginBottom: "20px"
            }}
        >

            <Link to="/">
                🎬 CineMind AI
            </Link>

            {" | "}

            {!token ? (
                <>
                    <Link to="/login">
                        Login
                    </Link>

                    {" | "}

                    <Link to="/register">
                        Register
                    </Link>
                </>
            ) : (
                <>
                    <span>
                        👤 {user?.username}
                    </span>

                    {" | "}

                    <Link to="/favorites">
                        ❤️ Favorites
                    </Link>

                    {" | "}

                    <button onClick={handleLogout}>
                        Logout
                    </button>
                </>
            )}

        </nav>
    );
}

export default Navbar;