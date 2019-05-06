import styled from "styled-components";

import Props from "./props";

export const List = styled.ul`
    display: ${(props: Props) => props.show ? "flex" : "none"};
    list-style: none;
    margin-left: 10px;
    background: white;
    padding-left: 20px;
    position: absolute;
    right: 0;
`;

export const Item = styled.li`
    margin-right: 20px;
    
    &:hover {
      cursor: pointer;
    }
`;
