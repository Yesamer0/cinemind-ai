import { Link, useNavigate } from "react-router-dom";

function Navbar() {

    const navigate = useNavigate();

    const token = localStorage.getItem("token");

    let user = null;

    try {
        user = JSON.parse(
            localStorage.getItem("user")
        );
    } catch {
        user = null;
    }


    function handleLogout() {

        localStorage.removeItem("token");
        localStorage.removeItem("user");

        navigate("/login");
    }


    return (
        <nav className="navbar">

            <div className="navbar-container">

                {/* LOGO */}

                <Link
                    to="/"
                    className="navbar-logo"
                >
                    <div className="navbar-logo-icon">
                        🎬
                    </div>

                    <div>
                        <span>CineMind</span>
                        <strong>AI</strong>
                    </div>
                </Link>


                {/* RIGHT SIDE */}

                <div className="navbar-links">

                    <Link
                        to="/"
                        className="navbar-link"
                    >
                        Home
                    </Link>


                    {!token ? (
                        <>
                            <Link
                                to="/login"
                                className="navbar-link"
                            >
                                Login
                            </Link>

                            <Link
                                to="/register"
                                className="navbar-register"
                            >
                                Get Started
                            </Link>
                        </>
                    ) : (
                        <>
                            <Link
                                to="/favorites"
                                className="navbar-link"
                            >
                                ❤️ Favorites
                            </Link>

                            <div className="navbar-user">
                                <span className="user-avatar">
                                    👤
                                </span>

                                <span>
                                    {user?.username || "User"}
                                </span>
                            </div>

                            <button
                                className="navbar-logout"
                                onClick={handleLogout}
                            >
                                Logout
                            </button>
                        </>
                    )}

                </div>

            </div>

        </nav>
    );
}

export default Navbar;