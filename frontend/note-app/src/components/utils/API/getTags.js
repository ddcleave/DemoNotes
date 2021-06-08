import { baseurl } from "./baseurl"
import refreshAPI from "./refresh"

export default async function getTagsAPI() {
  const url = '/note/tags'
  const response = await refreshAPI(
    async () => await fetch(baseurl + url)
  )
  return response
}