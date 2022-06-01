import React, {useState} from "react";

import {Navbar} from "./components/Navbar";
import {Footer} from "./components/Footer";
import {Routesp} from "./components/MyRoutes";

const App = () => {

    const [darkTheme, setDarkTheme] = useState(true);

    return (
        <div className={darkTheme ? 'dark' : ''}>
            <div className="dark:bg-gray-900 bg-gray-100 dark:text-gray-200 black min-h-screen">
                <Navbar darkTheme={darkTheme} setDarkTheme={setDarkTheme} />
                <Routesp />
                <Footer />
            </div>
        </div>
    );
}

export default App;