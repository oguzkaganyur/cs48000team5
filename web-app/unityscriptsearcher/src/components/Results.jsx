import React, {useEffect} from "react";
import {useLocation} from "react-router-dom";
import {useResultContext} from "../contexts/ResultContextProvider";
import {Loading} from "./Loading";

export const Results = () => {
    const {results, loading, getResults, searchTerm} = useResultContext();
    const location = useLocation();

    useEffect(() => {
        if (searchTerm !== '') {
            if (location.pathname === '/videos') {
                getResults(`/search/q=${searchTerm} videos`);
            } else {
                getResults(`${location.pathname}/q=${searchTerm}&num=40`);
            }
        }
    }, [searchTerm, location.pathname]);

    console.log(location.pathname);

    console.log("results", results);
    if(loading) return <Loading />;

    switch (location.pathname) {

        case '/search':
            return (
                <div className="sm:px-56 flex flex-wrap justify-between space-y-6">
                    {results?.results?.map(({ _source }, index) => (
                        <div key={index} className="md:w-2/5 w-full">
                            <a href={_source.function_url} target="_blank" rel="noreferrer">
                                <p className="text-sm">{_source.function_url.length > 60 ? _source.function_url.substring(0, 60) : _source.function_url}</p>
                                <p className="text-lg hover:underline dark:text-blue-300 text-blue-700  ">{_source.function_name}</p>
                            </a>
                        </div>
                    ))}
                </div>
            );
        default:
            return 'Error...';
    }
}










/*
import React, {useEffect} from "react";
import {useLocation} from "react-router-dom";
import {useResultContext} from "../contexts/ResultContextProvider";
import {Loading} from "./Loading";

export const Results = () => {
    const {results, loading, getResults, searchTerm} = useResultContext();
    const location = useLocation();

    useEffect(() => {
        if (searchTerm !== '') {
            if (location.pathname === '/videos') {
                getResults(`/search/q=${searchTerm} videos`);
            } else {
                getResults(`${location.pathname}/q=${searchTerm}&num=40`);
            }
        }
    }, [searchTerm, location.pathname]);

    console.log(location.pathname);
    if(loading) return <Loading />;

    switch (location.pathname) {
        case '/search':
            return (
                <div className="sm:px-56 flex flex-wrap justify-between space-y-6">
                    {results?.results?.map(({ link, title }, index) => (
                        <div key={index} className="md:w-2/5 w-full">
                            <a href={link} target="_blank" rel="noreferrer">
                                <p className="text-sm">{link.length > 30 ? link.substring(0, 30) : link}</p>
                                <p className="text-lg hover:underline dark:text-blue-300 text-blue-700  ">{title}</p>
                            </a>
                        </div>
                    ))}
                </div>
            );
        default:
            return 'Error...';
    }
}
 */