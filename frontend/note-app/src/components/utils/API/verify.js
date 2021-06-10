import { baseurl } from "./baseurl"

export default async function verifyAPI(token) {
  const url = '/api/v1/verify'
  const response = await fetch(baseurl + url, {
    method: "post",
    body: JSON.stringify({ "token": token })
  })
  return response
}