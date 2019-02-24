import axios from "axios";

import { IEntry, IFeed, EntryState } from "./models";

const entryStateURL = "/api/v1/feeds/state/";
const dashboardURL = "/api/v1/feeds/dash/";

export interface IEntryStateAction {
    state: EntryState;
    entry_id: number;
}

export const apiDeleteEntry = (id: number) => {
    const actions = [{ state: EntryState.Deleted, entry_id: id }];
    return apiModifyEntryStates(actions);
};

export const apiDeleteEntries = (ids: number[]) => {
    const actions = ids.map(id => {
        return { state: EntryState.Deleted, entry_id: id };
    });
    return apiModifyEntryStates(actions);
};

export const apiPinEntry = (id: number) => {
    const actions = [{ state: EntryState.Pinned, entry_id: id }];
    return apiModifyEntryStates(actions);
};

export const apiPinEntries = (ids: number[]) => {
    const actions = ids.map(id => {
        return { state: EntryState.Pinned, entry_id: id };
    });
    return apiModifyEntryStates(actions);
};

export const apiSaveEntry = (id: number) => {
    const actions = [{ state: EntryState.Saved, entry_id: id }];
    return apiModifyEntryStates(actions);
};

export const apiSaveEntries = (ids: number[]) => {
    const actions = ids.map(id => {
        return { state: EntryState.Saved, entry_id: id };
    });
    return apiModifyEntryStates(actions);
};

export const apiModifyEntryStates = (actions: IEntryStateAction[]) => {
    return axios.post(entryStateURL, { actions });
};

export interface IDashboardResult {
    entries: IEntry[];
    feed: IFeed;
}

export interface IDashboardResponse {
    results: IDashboardResult[];
}

export const apiGetDashboard = async (): Promise<IDashboardResult[]> => {
    const response = await axios.get(dashboardURL);
    const data = (response.data as IDashboardResponse);
    return data.results;
};
