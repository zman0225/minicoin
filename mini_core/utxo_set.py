import logging

from typing import Mapping
from mini_core.transaction import OutPoint, UnspentTxOut


logger = logging.getLogger(__name__)

utxo_set: Mapping[OutPoint, UnspentTxOut] = {}


def add_to_utxo(txout, tx, idx, is_coinbase, height):
  utxo = UnspentTxOut(*txout, txid=tx.id, txout_idx=idx, is_coinbase=is_coinbase, height=height)

  logger.info(f'adding tx outpoint {utxo.outpoint} to utxo_set')
  utxo_set[utxo.outpoint] = utxo


def rm_from_utxo(txid, txout_idx):
  del utxo_set[OutPoint(txid, txout_idx)]


def find_utxo_in_list(txin, txns) -> UnspentTxOut:
  txid, txout_idx = txin.outpoint
  try:
    txout = [t for t in txns if t.id == txid][0].txouts[txout_idx]
  except Exception as e:
    return None

  return UnspentTxOut(*txout, txid=txid, is_coinbase=False, height=-1, txout_idx=txout_idx)


