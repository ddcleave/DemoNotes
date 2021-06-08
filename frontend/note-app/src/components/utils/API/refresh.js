import { fpPromise } from "../../.."
import { baseurl } from "./baseurl"

export default async function refreshAPI(fn) {
  const response = await fn()
  if (response.status === 401) {
    const refresh_url = '/api/v1/refresh'
    const fp = await fpPromise
    const result = await fp.get()
    const visitorID = result.visitorId
    const data = new FormData()
    data.append("fingerprint", visitorID)
    const refresh_response = await fetch(baseurl + refresh_url, {
      method: "post",
      headers: {},
      body: data
    })
    if (refresh_response.ok) {
      const new_resp = await fn()
      return new_resp
    }
    else {
      return response
    }
  }
  else if (response.ok) {
    return response
  }
}