import { sequence } from "@sveltejs/kit/hooks";
import { handle as authHandle } from "./auth";
import { handleSession } from "./handleSession";
import { handleToken } from "./handleToken";
import { handleFetchClient } from "$lib/hooks/handleClient";

// Combined handle using sequence
export const handle = sequence(authHandle, handleFetchClient, handleToken, handleSession);
