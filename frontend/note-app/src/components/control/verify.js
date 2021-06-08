import { useEffect } from "react";
import { useHistory, useLocation } from "react-router";
import verifyAPI from "../utils/API/verify";

function useQuery() {
    return new URLSearchParams(useLocation().search);
}

export default function VerifyEmail() {
    let history = useHistory();
    const query = useQuery()

    async function verify() {
        if (query.get("token")) {
            const response = verifyAPI(query.get("token"))
            history.push("/")
        } else {
            history.push("/")
        }
    }
    
    useEffect(() => {
        verify()
    }, [])

    return (
        <div></div>
    )
}