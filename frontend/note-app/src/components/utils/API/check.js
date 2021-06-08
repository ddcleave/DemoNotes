import { baseurl } from "./baseurl"
import refreshAPI from "./refresh"

export default async function checkAPI() {
  const url = '/note/check'
  const response = await refreshAPI(
    async () => await fetch(baseurl + url)
  )
  return response
}