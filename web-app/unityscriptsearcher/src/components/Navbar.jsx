import React from "react";
import {Link} from 'react-router-dom';
import {Search} from "./Search";

//Unity Script Searcher 🔎

export const Navbar = ({ setDarkTheme, darkTheme }) => (
    <div className="p-5 pb-0 flex flex-wrap sm:justify-between justify-center items-center border-b dark:border-gray-700 border-gray-200 ">
        <div className="flex justify-between items-center space-x-5 w-screen ">
            <Link to="/">
                <img className='object-cover h-20 w-20' src={require('../assets/USS.png')} />
            </Link>
            <button type="button" onClick={() => setDarkTheme(!darkTheme)} className="text-xl dark:bg-gray-50 dark:text-gray-900 bg-white border rounded-full px-2 py-1 hover:shadow-lg">{darkTheme ? '💡 Light' : '🌙 Dark'}</button>
        </div>
        <Search />
    </div>
);