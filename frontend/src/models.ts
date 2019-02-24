export interface IFeed {
    id: number;
    title: string;
    link: string;
}

export interface IEntry {
    id: number;
    feed: IFeed;
    title: string;
    link: string;
    content: string;
    summary: string;
    date_published: string;
    states: EntryState[];
}

export enum EntryState {
    Saved = "saved",
    Deleted = "deleted",
    Pinned = "pinned",
}
