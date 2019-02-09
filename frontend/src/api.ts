import axios from "axios";

import { EntryState } from "./models";

const entryStateURL = "/api/v1/feeds/state/";

export interface IEntryStateAction {
    state: EntryState;
    entry_id: number;
}

export const deleteEntry = (id: number) => {
    const actions = [{ state: EntryState.Deleted, entry_id: id }];
    return modifyEntryStates(actions);
};

export const deleteEntries = (ids: number[]) => {
    const actions = ids.map(id => {
        return { state: EntryState.Deleted, entry_id: id };
    });
    return modifyEntryStates(actions);
};

export const pinEntry = (id: number) => {
    const actions = [{ state: EntryState.Pinned, entry_id: id }];
    return modifyEntryStates(actions);
};

export const pinEntries = (ids: number[]) => {
    const actions = ids.map(id => {
        return { state: EntryState.Pinned, entry_id: id };
    });
    return modifyEntryStates(actions);
};

export const saveEntry = (id: number) => {
    const actions = [{ state: EntryState.Saved, entry_id: id }];
    return modifyEntryStates(actions);
};

export const saveEntries = (ids: number[]) => {
    const actions = ids.map(id => {
        return { state: EntryState.Saved, entry_id: id };
    });
    return modifyEntryStates(actions);
};

export const modifyEntryStates = (actions: IEntryStateAction[]) => {
    return axios.post(entryStateURL, { actions });
};
