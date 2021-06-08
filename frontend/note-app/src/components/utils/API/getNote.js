import { baseurl } from "./baseurl"
import refreshAPI from "./refresh"

export default async function getNoteAPI(id) {
  const url = `/note/note/${id}`
  const response = await refreshAPI(
    async () => await fetch(baseurl + url)
  )
  return response
}