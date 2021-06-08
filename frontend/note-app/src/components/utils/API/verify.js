import { baseurl } from "./baseurl"

export default async function verifyAPI(token) {
  const url = '/api/v1/verify'
  const data = new FormData()
  data.append("token", token)
  const response = await fetch(baseurl + url, {
    method: "post",
    body: data
  })
  return response
}