import { Navigate, Route, Routes } from 'react-router-dom';
import {useEffect} from "react";

import { Results } from './Results';

export const Routesp = () => (
    <div className="p-4">

        <Routes>
            <Route path="/">
            </Route>
            <Route path="/search" element={<Results/>}/>
            <Route path="/images" element={<Results/>}/>
            <Route path="/news" element={<Results/>}/>
            <Route path="/videos" element={<Results/>}/>
        </Routes>
    </div>

);

/*

import React from "react";
import {Routes, Route, Navigate} from "react-router-dom";
import {Results} from "./Results";

export const Routess = () => {
    return (
        <div className="p-4">
            <Routes>
                <Route exact path="/">
                   <Navigate to="/search" />
                </Route>
                <Route path={['/search', '/images', '/news', '/videos']}>
                    <Results />
                </Route>
            </Routes>
        </div>
    );
}
 */