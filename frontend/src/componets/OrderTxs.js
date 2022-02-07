import * as React from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import Link from '@mui/material/Link';

export default function PinnedSubheaderList(props) {
  const { orderTxs } = props

  return (
    <div>
    <p style={{display: 'flex', flexDirection: 'column', boxAlign: 'center', alignItems: 'center'}}>Txs</p>
    <List
      sx={{
        width: '100%',
        bgcolor: 'background.paper',
        // position: 'relative',
        overflow: 'auto',
        maxHeight: 300,
        // '& ul': { padding: 0 },
      }}
    >
        {orderTxs.map((tx) => (
          <ListItem key={`item-${tx.id}`}>
              <Link href={`https://etherscan.io/tx/${tx.tx_hash}`} target="_blank"
                    underline="hover">{tx.created_at} {tx.type_tx}</Link>
          </ListItem>
        ))}
    </List>
  </div>
  );
}
