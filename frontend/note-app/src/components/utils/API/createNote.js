import { baseurl } from "./baseurl"
import refreshAPI from "./refresh"

export default async function createNoteAPI(data, tags) {
  const url = '/note/note/create'
  const newNote = {
    'note': JSON.stringify(data),
    'tags': tags
  }

  const response = await refreshAPI(
    async () => await fetch(baseurl + url, {
      method: "post",
      headers: {},
      body: JSON.stringify(newNote),
    })
  )
  return response
}