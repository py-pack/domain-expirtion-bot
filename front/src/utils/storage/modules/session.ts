import {createStorage} from '../localStorage'

const storage = createStorage('session')

const SESSION_ID_KEY: string = "session_id"

export function getSessionId(): string {
    let id: string = storage.read<string>({key: SESSION_ID_KEY})
    if (!id) {
        id = crypto.randomUUID()
        storage.write({key: SESSION_ID_KEY, value: id})
    }
    return id
}

export function clearSessionId(): void {
    storage.remove({key: SESSION_ID_KEY})
}
