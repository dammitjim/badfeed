import React, {useState} from "react";

import EntryRowSmall from "../entry-row-small/index";
import Props from "./props";

export default (props: Props) => {
    const [doneWithAll, setDoneWithAll] = useState(false);
    const handleMouseClick = (event: React.MouseEvent) => {
        if (!doneWithAll) {
            setDoneWithAll(true);
            if (props.demo) {
                setTimeout(() => setDoneWithAll(false), 2000)
            }
        }
    }

    let entries: Array<React.ReactElement>;
    if (doneWithAll) {
        entries = [];
    } else {
        entries = props.entries.map(entry => <EntryRowSmall entry={entry} />);
    }

    return (
        <div>
            {entries}

            <div>
                <button onClick={handleMouseClick}>Done.</button>
            </div>
        </div>
    )
}
